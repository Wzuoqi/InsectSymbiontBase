"""
Django settings for InsectSymbiontDB project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# STATIC SETTINGS
STATIC_URL = '/static/'

# BASE_DIR 是项目的绝对地址
STATIC_ROOT = os.path.join(BASE_DIR, 'collect_static')

#以下不是必须的  各个app共用的文件可以放在这
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'common_static'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9av7pfz%t@boo7#x7u($n%=gs2wou$ciw1a&1_embk_+qkn7=u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

ADMIN_EMAIL = "wangzuoqi@zju.edu.cn"  # 替换为您的邮箱
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'symbiont',
    'metagenome',
    'amplicon',
    'article',
    'genome',
    'gene',
    'feedback',
    'tailwind',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'InsectSymbiontDB.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'InsectSymbiontDB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'insectsymbiontbase',
        'USER': 'zju',
        'PASSWORD': 'zijin1201',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Download directories
DOWNLOADS_ROOT = os.path.join(MEDIA_ROOT, 'downloads')
GENOMES_ROOT = os.path.join(DOWNLOADS_ROOT, 'genomes')
DATASETS_ROOT = os.path.join(DOWNLOADS_ROOT, 'datasets')
DOCUMENTS_ROOT = os.path.join(DOWNLOADS_ROOT, 'documents')

# Create directories if they don't exist
os.makedirs(GENOMES_ROOT, exist_ok=True)
os.makedirs(DATASETS_ROOT, exist_ok=True)
os.makedirs(DOCUMENTS_ROOT, exist_ok=True)

# 在现有的 MEDIA_ROOT 配置下添加
BATCH_SEARCH_ROOT = os.path.join(MEDIA_ROOT, 'batch_search')
BATCH_SEARCH_TEMP = os.path.join(BATCH_SEARCH_ROOT, 'temp')
BATCH_SEARCH_RESULTS = os.path.join(BATCH_SEARCH_ROOT, 'results')

# 创建必要的目录
os.makedirs(BATCH_SEARCH_TEMP, exist_ok=True)
os.makedirs(BATCH_SEARCH_RESULTS, exist_ok=True)
