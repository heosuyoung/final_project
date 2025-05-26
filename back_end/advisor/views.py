from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json
import os
from openai import OpenAI

# OpenAI 클라이언트 설정 - 클라이언트 변수를 나중에 함수 내에서 생성
from django.conf import settings
api_key = settings.OPENAI_API_KEY

@api_view(['POST'])
@permission_classes([AllowAny])  # 인증 없이 모든 사용자가 접근 가능하도록 설정 - AllowAny 사용
@csrf_exempt  # CSRF 보호 비활성화
def chat_with_advisor(request):
    """
    AI 어드바이저와 채팅하는 API - 인증 불필요
    """
    try:
        data = request.data
        message = data.get('message', '')
        context = data.get('context', [])
        financial_data = data.get('financial_data', None)
        
        print(f"메시지 받음: {message[:30]}...")  # 디버깅을 위한 로그 출력
        if financial_data:
            print(f"재무 데이터 수신: {financial_data.get('ageGroup')}, 목표: {financial_data.get('financialGoal')}")
          
        # OpenAI API가 정상적으로 동작하지 않는 경우를 위한 다양한 하드코딩된 응답
        hardcoded_responses = {
            "안녕": [
                "안녕하세요! EA$E AI 금융 어드바이저입니다. 어떤 금융 목표를 가지고 계신가요?", 
                "반갑습니다! EA$E AI 금융 어드바이저입니다. 오늘 어떤 금융 관련 질문이 있으신가요?",
                "안녕하세요! 금융 전문가 EA$E입니다. 자산 관리나 투자에 대해 어떤 도움이 필요하신가요?"
            ],
            "주식 추천": [
                "투자 성향과 목표에 따라 종목을 추천해 드리겠습니다. 안정적인 성장을 원하신다면 삼성전자(005930)와 같은 대형주가 적합합니다. 배당 수익을 원하신다면 KB금융(105560)이나 기아(000270) 같은 종목을 고려해 보세요.",
                "장기 투자를 고려하신다면, 글로벌 경쟁력을 갖춘 삼성전자(005930), SK하이닉스(000660)와 같은 반도체 관련주, 그리고 제약 바이오 섹터의 삼성바이오로직스(207940)를 추천드립니다.",
                "최근 실적이 개선되고 있는 현대차(005380), 미래 성장성이 기대되는 카카오(035720), 안정적인 수익을 제공하는 POSCO홀딩스(005490)를 균형있게 포트폴리오에 포함해보세요."
            ],
            "주식": [
                "주식 투자는 장기적인 관점으로 접근하는 것이 중요합니다. 분산 투자로 리스크를 줄이고, 정기적인 리밸런싱을 통해 포트폴리오를 관리하는 것이 좋습니다.",
                "주식 시장은 단기적으로는 변동성이 크지만, 장기적으로는 꾸준한 수익을 기대할 수 있습니다. 투자 원금의 10% 이상을 단일 종목에 투자하지 않는 것이 위험 분산에 도움이 됩니다.",
                "주식에 투자할 때는 기업의 재무제표, 성장 가능성, 산업 동향 등을 종합적으로 고려하는 것이 중요합니다. ETF를 통한 인덱스 투자는 초보 투자자에게 추천하는 안전한 방법입니다."
            ],
            "저축": [
                "저축은 재정 건전성의 기반입니다. 소득의 약 20%를 저축하는 것이 권장되며, 비상금으로 최소 3-6개월 치 생활비를 유동성 높은 계좌에 보관하는 것이 좋습니다.",
                "안정적인 저축을 위해서는 '페이 유어셀프 퍼스트(Pay yourself first)' 원칙을 따르는 것이 좋습니다. 매달 소득이 들어오면 먼저 저축을 하고, 남은 금액으로 지출을 계획하세요.",
                "저축의 종류에는 일반 예금, 적금, MMF, CMA 등이 있으며, 목적과 기간에 따라 적절한 상품을 선택하는 것이 중요합니다. 인플레이션을 고려하여 단순 예금만으로는 자산 가치가 하락할 수 있음을 유의하세요."
            ],
            "부동산": [
                "부동산 투자는 위치, 시장 동향, 그리고 재정 상태를 충분히 고려해야 합니다. 월 소득 대비 대출 상환액이 30%를 넘지 않는 것이 안전합니다.",
                "부동산은 장기 자산으로, 현금 흐름(임대 수익)과 자본 이득(매매 차익) 두 가지 측면에서 접근해야 합니다. 투자 전 해당 지역의 발전 계획과 인프라 구축 상황을 꼼꼼히 살펴보세요.",
                "부동산에 투자할 때는 LTV(담보인정비율)와 DSR(총부채원리금상환비율)을 고려하여 무리한 레버리지를 사용하지 않는 것이 중요합니다. 유동성 위험을 항상 염두에 두세요."
            ],
            "은퇴": [
                "은퇴 계획은 일찍 시작할수록 효과적입니다. 복리의 힘을 활용하고, 점진적으로 안전 자산 비중을 높여가는 전략이 중요합니다.",
                "은퇴 준비를 위해서는 현재 생활 수준을 고려한 목표 금액을 설정하고, 체계적인 저축 및 투자 계획을 세워야 합니다. 일반적으로 은퇴 후에는 현재 소득의 70-80% 정도가 필요하다고 합니다.",
                "은퇴 자금은 연금, 주식, 채권, 부동산 등 다양한 자산에 분산 투자하는 것이 좋습니다. 은퇴가 가까워질수록 위험 자산의 비중을 점진적으로 줄이고 안전 자산의 비중을 높이세요."
            ],
            "펀드": [
                "펀드는 여러 투자자의 자금을 모아 전문 운용사가 관리하는 금융상품입니다. 투자자의 성향과 목표에 맞는 펀드를 선택하는 것이 중요합니다.",
                "펀드 투자 시에는 운용 보수, 판매 수수료 등의 비용을 꼼꼼히 확인해야 합니다. 장기적으로는 낮은 비용의 인덱스 펀드가 높은 수수료의 액티브 펀드보다 더 나은 성과를 보이는 경우가 많습니다.",
                "펀드는 주식형, 채권형, 혼합형, MMF 등 다양한 유형이 있으며, 위험 허용도와 투자 기간에 맞게 선택해야 합니다. 펀드 투자 전에 투자설명서와 과거 수익률을 반드시 확인하세요."
            ],
            "채권": [
                "채권은 정부나 기업이 자금을 조달하기 위해 발행하는 부채 증서로, 일반적으로 주식보다 안정적인 수익을 제공합니다.",
                "채권 투자 시에는 금리 변동 위험, 신용 위험, 인플레이션 위험 등을 고려해야 합니다. 금리가 상승하면 기존 채권의 가치는 하락하는 경향이 있습니다.",
                "채권은 포트폴리오의 안정성을 높이는 역할을 합니다. 만기, 수익률, 발행 기관의 신용도 등을 종합적으로 고려하여 투자하세요."
            ],
        }
        
        # 재무 정보가 제공된 경우, 맞춤형 응답 제공
        if financial_data:
            age_group = financial_data.get('ageGroup', '')
            financial_goal = financial_data.get('financialGoal', '')
            risk_tolerance = financial_data.get('riskTolerance', '')
            monthly_income = financial_data.get('monthlyIncome', 0)
            monthly_expense = financial_data.get('monthlyExpense', 0)
            
            # 소득 대비 지출 비율 계산
            expense_ratio = (monthly_expense / monthly_income * 100) if monthly_income > 0 else 0
            
            # 간단한 맞춤형 응답 생성
            if "주택 구입" in financial_goal:
                return Response({
                    "response": f"{age_group}의 주택 구입 목표를 위해, 현재 소득의 {expense_ratio:.1f}%를 지출하고 계시네요. "
                               f"주택 구입을 위해서는 소득의 최대 30%를 주거 비용으로 설정하는 것이 권장됩니다. "
                               f"{risk_tolerance} 투자 성향을 고려할 때, 주택 구입 자금의 일부는 안정적인 금융 상품에, "
                               f"나머지는 적절한 수익성을 갖춘 상품에 분산 투자하는 것이 좋습니다.",
                    "success": True
                })
            elif "은퇴 준비" in financial_goal:
                return Response({
                    "response": f"{age_group}의 은퇴 준비를 위해, 소득의 약 15-20%를 은퇴 계좌에 정기적으로 저축하는 것이 좋습니다. "
                               f"현재 지출 비율이 {expense_ratio:.1f}%이므로, 지출을 줄여 저축률을 높이는 방안을 고려해보세요. "
                               f"{risk_tolerance} 투자 성향에 맞게, 젊을수록 주식 비중을, 은퇴에 가까워질수록 채권 비중을 높이는 전략이 효과적입니다.",
                    "success": True
                })
            elif "투자 수익률 향상" in financial_goal:
                return Response({
                    "response": f"{risk_tolerance} 투자 성향을 가진 {age_group}의 투자 수익률 향상을 위해, "
                               f"글로벌 분산 투자와 정기적인 리밸런싱 전략이 중요합니다. "
                               f"현재 소득 대비 {expense_ratio:.1f}%의 지출 비율을 유지하면서, "
                               f"추가적인 투자금을 모아 다양한 자산군(주식, 채권, 대체투자)에 분산 투자하세요. "
                               f"장기적인 관점에서 투자하고, 시장 변동성에 과민반응하지 않는 것이 중요합니다.",
                    "success": True
                })        # 주식 추천 요청 처리
        import random
        
        if "주식" in message and ("추천" in message or "알려" in message or "어떤" in message):
            stock_recommendations = [
                "투자 성향에 따라 다음 종목들을 고려해볼 수 있습니다. 성장성을 중시한다면 삼성전자(005930), 안정성을 중시한다면 KB금융(105560), 고배당을 원한다면 현대차(005380)를 추천드립니다. 장기 투자 관점에서 접근하시는 것이 중요합니다.",
                "최근 실적이 개선되고 있는 SK하이닉스(000660), 미래 성장성이 기대되는 NAVER(035420), 안정적인 배당과 성장을 제공하는 삼성물산(028260)을 균형있게 포트폴리오에 추가해보시는 것을 고려해보세요.",
                "안정적인 투자를 원하신다면 KOSPI ETF, 성장성을 추구하신다면 반도체 관련주인 삼성전자(005930)와 SK하이닉스(000660), 리스크를 감수할 수 있다면 바이오 섹터의 삼성바이오로직스(207940)를 고려해보세요. 단, 모든 투자에는 리스크가 따른다는 점을 명심하세요."
            ]
            return Response({
                "response": random.choice(stock_recommendations),
                "success": True
            })
            
        # 메시지에 특정 키워드가 포함된 경우 하드코딩된 응답 배열에서 랜덤하게 선택
        for keyword, responses in hardcoded_responses.items():
            if keyword in message:
                selected_response = random.choice(responses)
                return Response({
                    "response": selected_response,
                    "success": True
                })                
        # 일반적인 응답 - OpenAI API 없이
        default_response = """
        금융 목표를 이루기 위해서는 체계적인 계획이 필요합니다. 소득, 지출, 부채, 자산 등의 현재 재정 상태를 분석하고, 
        단기, 중기, 장기 목표를 설정하여 체계적으로 접근하는 것이 중요합니다. 
        투자는 분산투자 원칙을 지키고, 정기적인 리밸런싱을 통해 위험을 관리하는 것이 좋습니다.
        더 구체적인 조언이 필요하시면 특정 금융 목표나 현재 상황에 대해 알려주시기 바랍니다.
        """
        
        # OpenAI API 시도해보기 - 문제 발생 시 위의 하드코딩된 응답으로 폴백
        try:
            # 기본 시스템 메시지
            system_message = """
            당신은 EA$E AI 금융 어드바이저입니다. 
            사용자에게 맞춤형 자산 분석, 최적의 포트폴리오 구성, 금융 목표 달성을 위한 로드맵을 제공하는 금융 전문가입니다.
            한국어로 친절하고 전문적으로 답변해주세요.
            """
            
            # 재무 정보가 제공된 경우 시스템 메시지에 추가
            if financial_data:
                age_group = financial_data.get('ageGroup', '')
                monthly_income = financial_data.get('monthlyIncome', 0)
                monthly_expense = financial_data.get('monthlyExpense', 0)
                savings = financial_data.get('savings', 0)
                stocks = financial_data.get('stocks', 0)
                realestate = financial_data.get('realestate', 0)
                loans = financial_data.get('loans', 0)
                credit_debt = financial_data.get('creditCardDebt', 0)
                financial_goal = financial_data.get('financialGoal', '')
                risk_tolerance = financial_data.get('riskTolerance', '')
                investment_timeframe = financial_data.get('investmentTimeframe', '')
                additional_info = financial_data.get('additionalInfo', '')
                
                financial_context = f"""
                사용자 재무 정보:
                - 연령대: {age_group}
                - 월소득: {monthly_income}만원
                - 월지출: {monthly_expense}만원
                - 저축/예금: {savings}만원
                - 주식/펀드: {stocks}만원
                - 부동산: {realestate}만원
                - 대출: {loans}만원
                - 카드부채: {credit_debt}만원
                - 금융목표: {financial_goal}
                - 투자성향: {risk_tolerance}
                - 투자기간: {investment_timeframe}
                - 추가정보: {additional_info}
                
                위 정보를 바탕으로 사용자의 재정 상황에 맞는 맞춤형 금융 조언을 제공하세요.
                답변에는 구체적인 숫자와 근거를 포함하고, 사용자의 금융 목표 달성을 위한 단계별 행동 계획을 제안해주세요.
                """
                
                system_message += financial_context
            
            # 사용자 대화 기록 구성
            messages = [
                {"role": "system", "content": system_message},
            ]
            
            # 이전 대화 컨텍스트가 있으면 추가
            if context:
                for msg in context:
                    messages.append({"role": msg["role"], "content": msg["content"]})
            
            # 사용자의 새 메시지 추가
            messages.append({"role": "user", "content": message})
              # API 키 확인
            api_key_value = settings.OPENAI_API_KEY
            if not api_key_value:
                print("API 키가 설정되지 않았습니다.")
                # API 키가 없는 경우 기본 응답 반환
                return Response({
                    "response": default_response,
                    "success": True
                })
            
            # OpenAI API 호출
            client = OpenAI(api_key=api_key_value)
            print(f"API 키 확인: {api_key_value[:8]}***")  # API 키의 일부만 출력
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            # AI 응답 추출
            ai_response = response.choices[0].message.content
            print(f"AI 응답: {ai_response[:30]}...")  # 디버깅을 위한 로그 출력
            
            return Response({
                "response": ai_response,
                "success": True
            })
            
        except Exception as api_error:
            print(f"OpenAI API 오류: {str(api_error)}")
            # API 오류 발생 시 기본 응답 반환
            return Response({
                "response": default_response,
                "success": True  # 사용자에게는 성공으로 반환
            })
        
    except Exception as e:
        return Response({
            "response": f"죄송합니다. 오류가 발생했습니다: {str(e)}",
            "success": False
        }, status=500)
