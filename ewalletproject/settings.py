"""
Django settings for ewalletproject project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# https host should be at the end of list
ALLOWED_HOSTS = ["127.0.0.1",env("HOST_DOMAIN")]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     # external libraries
    'rest_framework',
    "corsheaders",
    # register accounts app
    'accounts.apps.AccountsConfig',
    # register payments app
    'payments.apps.PaymentsConfig',

]


REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

     # add cors middleware
    "corsheaders.middleware.CorsMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# cors origins settings
CORS_ALLOW_ALL_ORIGINS = True
# # CORS_ALLOWED_ORIGINS = [
# #     "http://read.only.com",
# #     "http://change.allowed.com",
#     "https://sandbox.safaricom.co.ke",
      
# # ]

# CSRF_TRUSTED_ORIGINS = [
#     "https://sandbox.safaricom.co.ke",
# ]

ROOT_URLCONF = 'ewalletproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ewalletproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# mpesa configs
CONFIRMATIONURL = f"https://{ALLOWED_HOSTS[-1]}/api/v1/payments/c2b_confirmation_hook"
VALIDATIONURL = f"https://{ALLOWED_HOSTS[-1]}/api/v1/payments/c2b_validation_hook"
STKPUSH_CALLBACKURL = f"https://{ALLOWED_HOSTS[-1]}/api/v1/payments/stk_push_webhook"

print(CONFIRMATIONURL)
print(VALIDATIONURL)

SHORTCODE=env("SHORTCODE")
# for simulating c2b transactions
TESTMSISDN=env("TESTMSISDN")
CONSUMER_KEY=env("CONSUMER_KEY")
CONSUMER_SECRET=env("CONSUMER_SECRET")
PASSKEY=env("PASSKEY")

MPESA_AUTH_URL=env("MPESA_AUTH_URL")
MPESA_REGISTER_CALLBACK_URL=env("MPESA_REGISTER_CALLBACK_URL")
PROCESS_STKPUSH_URL=env("PROCESS_STKPUSH_URL")
C2B_SIMULATE_URL=env("C2B_SIMULATE_URL")
