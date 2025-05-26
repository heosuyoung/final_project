import openai
import environ

env = environ.Env()
env.read_env('.env')
openai.api_key = env("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # gpt-4o-mini 모델 사용
    messages=[
        {"role": "user", "content": "안녕하세요, 연결 테스트입니다."}
    ]
)

print("✅ 응답:", response.choices[0].message['content'])
