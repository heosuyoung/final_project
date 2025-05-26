"""
OpenAI API 연결 테스트 스크립트

이 스크립트는 OpenAI API 연결을 테스트하여 API 키가 올바르게 작동하는지 확인합니다.
"""

import os
import sys
from openai import OpenAI
import json

# API 키 설정

def test_openai_connection():
    """OpenAI API 연결 테스트"""
    print("OpenAI API 연결 테스트 시작...")
    
    try:
        # API 클라이언트 초기화
        client = OpenAI(api_key=API_KEY)
        
        # 간단한 API 호출 테스트
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 EA$E AI 금융 어드바이저입니다."},
                {"role": "user", "content": "안녕하세요, API 연결 테스트입니다."}
            ],
            temperature=1,
            max_tokens=100
        )
        
        # 응답 출력
        message_content = response.choices[0].message.content
        print("\n✅ API 연결 성공!")
        print(f"응답: {message_content}")
        
        # API 응답 구조 출력
        print("\n응답 구조:")
        print(f"- 모델: {response.model}")
        print(f"- 사용된 토큰: {response.usage.total_tokens}")
        print(f"- 완료 여부: {response.choices[0].finish_reason}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ API 연결 실패: {str(e)}")
        if hasattr(e, 'response'):
            print(f"오류 응답: {e.response}")
        return False

if __name__ == "__main__":
    test_openai_connection()
