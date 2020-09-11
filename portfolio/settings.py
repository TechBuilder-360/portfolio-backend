import os
import cloudinary
import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_BASE = os.path.abspath(os.path.join(BASE_DIR, 'portfolio'))

dotenv_file = os.path.join(BASE_DIR, ".keys")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


SECRET_KEY = os.getenv('PORTFOLIO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('PORTFOLIO_DEBUG')

ALLOWED_HOSTS = os.getenv('PORTFOLIO_ALLOWED_HOSTS').split(',')

# Application definition
AUTH_USER_MODEL = "accounts.User"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'resume',
    'accounts',
    'rest_framework',
    'cloudinary',
    'social_django',
    'graphene_django'
]

TEMPLATE_LOADERS = [
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_BASE, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('PORTFOLIO_DATABASE_ENGINE'),
        'NAME': os.getenv('PORTFOLIO_DATABASE_NAME'),
        'USER': os.getenv('PORTFOLIO_DATABASE_USER'),
        'PASSWORD': os.getenv('PORTFOLIO_DATABASE_PASSWORD'),
        'HOST': os.getenv('PORTFOLIO_DATABASE_HOST'),
        'PORT': os.getenv('PORTFOLIO_DATABASE_PORT')
    },
}

# LOGIN_URL = '/auth/login/google-oauth2/'

# LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = os.getenv('PORTFOLIO_STATIC_URL')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'portfolio', 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# add config
cloudinary.config(
    cloud_name=os.getenv('PORTFOLIO_CLOUD_NAME'),
    api_key=os.getenv('PORTFOLIO_API_KEY'),
    api_secret=os.getenv('PORTFOLIO_API_SECRET'),
    secure=True
)

SOCIAL_AUTH_USER_MODEL = 'accounts.User'

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/accounts/success/'
# SOCIAL_AUTH_LOGIN_URL = '/login-url/'
# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'
# SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('PORTFOLIO_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('PORTFOLIO_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'accounts.pipeline.get_avatar',
)

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

GRAPHENE = {
    "SCHEMA": "portfolio.schema.schema"
}
