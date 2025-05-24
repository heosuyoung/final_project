from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import requests
from .models import Board, Comment
from .forms import BoardForm, CommentForm


@require_http_methods(["GET"])
def index(request):
    boards = Board.objects.all().order_by('-created_at')
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)


@require_http_methods(["GET", "POST"])
def detail(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        if request.user == board.author:
            board.delete()
        return redirect('boards:index')

    comments = board.comments.all()
    comment_form = CommentForm()
    context = {
        'board': board,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'boards/detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if board.author != request.user:
        return redirect('boards:detail', pk)

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm(instance=board)
    context = {
        'board': board,
        'form': form,
    }
    return render(request, 'boards/update.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('boards:index')
    else:
        form = BoardForm()
    context = {
        'form': form,
    }
    return render(request, 'boards/create.html', context)


@login_required
@require_http_methods(["POST"])
def comment(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.board = board
        comment.author = request.user
        comment.save()
    return redirect('boards:detail', board.pk)


@login_required
@require_http_methods(["POST"])
def create_reply(request, comment_pk):
    comment = get_object_or_404(Comment, id=comment_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        reply_comment = form.save(commit=False)
        reply_comment.board = comment.board
        reply_comment.author = request.user
        reply_comment.parent_comment = comment
        reply_comment.save()
    return redirect("boards:detail", comment.board.id)


@login_required
@require_http_methods(["POST"])
def comment_detail(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.author == request.user:
        comment.delete()
    return redirect('boards:detail', board_pk)


@require_http_methods(["GET"])
def fetch_savings_products(request):
    """
    금융감독원 API를 호출하여 예금/적금 상품 정보를 필터링하고 반환합니다.
    
    파라미터:
        - type: 'deposit' (예금) 또는 'savings' (적금)
        - sort: 정렬 방식 ('rate' 등)
        - conditions[]: 우대조건 필터링 (리스트)
    """
    # 디버그 로그 추가
    print("\n================= API 호출 시작 =================")
    
    # 파라미터 받아오기
    product_type = request.GET.get('type', 'savings')  # 기본값은 적금
    sort = request.GET.get('sort', 'rate')  # 금리 기준 정렬
    conditions = request.GET.getlist('conditions[]')  # 우대조건 리스트
    
    print(f"요청 파라미터: type={product_type}, sort={sort}, conditions={conditions}")

    # API URL 설정 (예금/적금에 따라 다른 URL 사용)
    if product_type == 'deposit':
        base_url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    else:  # savings
        base_url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
    
    print(f"API URL: {base_url}")

    # API 요청 파라미터 설정
    params = {
        "auth": settings.FSS_API_KEY,
        "topFinGrpNo": "020000",  # 은행
        "pageNo": "1"
    }
    print(f"API 파라미터: {params}")
    
    try:
        # API 호출
        print("금융감독원 API 호출 중...")
        response = requests.get(base_url, params=params)
        print(f"API 응답 코드: {response.status_code}")

        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()
        
        print(f"API 응답 전체 구조: {data.keys()}")
        print(f"Result 구조: {data.get('result', {}).keys()}")

        # 에러 코드와 메시지 확인
        err_cd = data.get('result', {}).get('err_cd', 'Unknown')
        err_msg = data.get('result', {}).get('err_msg', 'Unknown')
        print(f"API 에러 코드: {err_cd}, 에러 메시지: {err_msg}")

        # 에러 메시지 디코딩
        try:
            decoded_err_msg = err_msg.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            decoded_err_msg = err_msg  # 디코딩 실패 시 원본 유지

        print(f"디코딩된 에러 메시지: {decoded_err_msg}")

        # 에러가 있는 경우 클라이언트에 반환 (성공 코드는 '000' 또는 '0000')
        if err_cd != '000' and err_cd != '0000':
            return JsonResponse({'error_code': err_cd, 'error_message': decoded_err_msg}, status=400)

        # 데이터 구조 확인 및 필터링
        base_list = data.get('result', {}).get('baseList', [])
        option_list = data.get('result', {}).get('optionList', [])

        # 데이터가 없는 경우 빈 배열 반환
        if not base_list or not option_list:
            print("API 응답에 baseList 또는 optionList가 없습니다.")
            return JsonResponse([], safe=False)

        print(f"API 응답 데이터: baseList 길이={len(base_list)}, optionList 길이={len(option_list)}")

        # 금융 상품 정보 구성
        filtered_products = []

        for product in base_list:
            product_info = {
                'fin_prdt_cd': product.get('fin_prdt_cd', ''),
                'kor_co_nm': product.get('kor_co_nm', ''),
                'fin_prdt_nm': product.get('fin_prdt_nm', ''),
                'join_way': product.get('join_way', ''),
                'mtrt_int': product.get('mtrt_int', ''),
                'spcl_cnd': product.get('spcl_cnd', ''),
                'join_deny': product.get('join_deny', ''),
                'options': []
            }

            for option in option_list:
                if option.get('fin_prdt_cd') == product_info['fin_prdt_cd']:
                    product_info['options'].append({
                        'intr_rate_type': option.get('intr_rate_type', ''),
                        'intr_rate': option.get('intr_rate', 0),
                        'intr_rate2': option.get('intr_rate2', 0),
                        'save_trm': option.get('save_trm', 0)
                    })

            if product_info['options']:
                filtered_products.append(product_info)

        print(f"필터링 후 상품 개수: {len(filtered_products)}")

        if sort == 'rate':
            filtered_products.sort(
                key=lambda x: max([float(opt.get('intr_rate2', 0)) for opt in x['options']]),
                reverse=True
            )

        print(f"최종 반환 상품 개수: {len(filtered_products)}")
        return JsonResponse(filtered_products, safe=False)

    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류: {str(e)}")
        return JsonResponse({'error': 'HTTP 요청 오류', 'details': str(e)}, status=500)

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return JsonResponse({'error': '서버 오류', 'details': str(e)}, status=500)


@login_required
def get_api_key(request):
    """
    금융감독원 API 키를 반환하는 뷰.
    """
    api_key = settings.FSS_API_KEY
    return JsonResponse({'api_key': api_key})
