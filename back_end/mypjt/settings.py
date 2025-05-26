import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(env_file=os.path.join(BASE_DIR, '.env'))  # .env 경로 명시

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)

FSS_API_KEY = env("FSS_API_KEY")
OPENAI_API_KEY = env("OPENAI_API_KEY")

# OpenAI API 키를 환경 변수에 설정
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'accounts',  # accounts 앱을 가장 먼저 배치
    'boards',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',  # 소셜 로그인 앱
    'corsheaders',    # CORS 미들웨어 추가
    'rest_framework', # Django REST Framework
    'rest_framework.authtoken', # 토큰 인증
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS 미들웨어를 가장 위에 추가
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # CSRF 미들웨어 비활성화
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # 소셜 미들웨어 추가
]

ROOT_URLCONF = 'mypjt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # 소셜 컨텍스트
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'mypjt.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.kakao.KakaoOAuth2',  # 카카오 로그인 추가
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

# 카카오 로그인 설정
SOCIAL_AUTH_KAKAO_KEY = env("SOCIAL_AUTH_KAKAO_KEY")
SOCIAL_AUTH_KAKAO_SECRET = env("SOCIAL_AUTH_KAKAO_SECRET", default="")
# 카카오 관련 추가 설정
SOCIAL_AUTH_KAKAO_EXTRA_DATA = ['nickname', 'profile_image']

# 소셜 로그인 관련 설정
LOGIN_REDIRECT_URL = 'http://localhost:5173/oauth/callback'
LOGOUT_REDIRECT_URL = 'http://localhost:5173/'

# 소셜 로그인 콜백 설정
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://localhost:5173/oauth/callback'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# 카카오 특정 리다이렉트 URL 설정
SOCIAL_AUTH_KAKAO_LOGIN_REDIRECT_URL = 'http://localhost:5173/oauth/callback'

# Google OAuth 추가 설정
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'approval_prompt': 'force'
}

# 카카오 로그인 추가 설정 - 필수 스코프만 사용 (권한 오류 방지)
SOCIAL_AUTH_KAKAO_SCOPE = ['profile_nickname', 'profile_image']
SOCIAL_AUTH_KAKAO_PROFILE_EXTRA_PARAMS = {  
    'fields': 'id, name, picture'
}

# 카카오 로그인 응답 처리 설정
SOCIAL_AUTH_KAKAO_AUTH_EXTRA_ARGUMENTS = {'prompt': 'login'}

# 커스텀 함수 설정
SOCIAL_AUTH_KAKAO_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'accounts.social_pipeline.create_user_token',
)

# 소셜 로그인 파이프라인 설정
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # 이메일로 기존 계정과 연동
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'accounts.social_pipeline.create_user_token',  # 사용자 토큰 생성 커스텀 파이프라인
)

# 디버깅 확인용 출력
print("✅ GOOGLE_CLIENT_ID =", env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"))

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF 설정
CSRF_TRUSTED_ORIGINS = ['http://localhost:5173', 'http://localhost:8000']
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = None

# REST Framework 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # SessionAuthentication은 CSRF 검증을 수행하므로 임시로 제거
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # AI 어드바이저와 같은 일부 API는 별도의 권한 설정을 통해 인증 없이 접근 가능
}
