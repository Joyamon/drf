"""
Django'Settings for drf project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import pytz

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u*_^ql)6%v5j54gfeojh$#(hy^8lh-hl0y(m__5r&-uk^6@+u&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'rest_framework',
    'django_celery_beat',
    'django_celery_results'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'drf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

################################################################
# rest_framework相关配置信息
################################################################

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'drf.pagination.CustomPagination',

    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'drf.custom_authentication.CustomAuthentication',  # 添加自定义认证类

    ],
    'VERSION_PARAM': 'version',  # 版本
}
################################################################
# logging相关配置信息
################################################################
import os
# 判断drf根目录下是否有logs文件夹，没有则创建
if not os.path.exists('logs'):
    os.mkdir('logs')
# 判断logs文件夹下是否有debug.log文件,没有则创建
if not os.path.exists('logs/debug.log'):
    open('logs/debug.log', 'w').close()
if not os.path.exists('logs/run.log'):
    open('logs/run.log', 'w').close()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] - %(funcName)s- %(lineno)d- %(message)s', }
        # 日志格式
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'maxBytes': 1024 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/run.log'),
            'maxBytes': 1024 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'scprits_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/run.log'),
            'maxBytes': 1024 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        'drf.app': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'INFO',
            'propagate': True
        },
        'drf': {
            'handlers': ['scprits_handler', 'console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
################################################################
# redis 相关配置
################################################################
REDIS_PASSWORD = ''
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:{REDIS_PORT}'

################################################################
# celery 相关配置
################################################################

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'{REDIS_URL}/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'socket_timeout': 5},  # 连接redis超时时间，单位为秒

        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
    }
}
# celery相关配置
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/2'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


# celery 时区
CELERY_TIMEZONE = TIME_ZONE
# CELERY_BROKER_URL = f'{REDIS_URL}/0'  # Broker配置，使用Redis作为消息中间件(无密码)
# CELERY_BROKER_URL = 'redis://:@127.0.0.1:6379/10'  #lybbn 代表 账号（没有可省略）  {} 存放密码  127.0.0.1连接的 ip  6379端口  10 redis库
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/11' # 把任务结果存在了Redis
# celery结果存储到数据库中django-db
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'  # Backend数据库
CELERY_RESULT_PERSISTENT = True
CELERY_RESULT_EXTENDED = True
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_ENABLE_UTC = False
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 连接超时
CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化使json
CELERY_RESULT_SERIALIZER = 'json'
# CELERYD_CONCURRENCY = 2  #并发worker数量
CELERY_WORKER_CONCURRENCY = 2  # 并发数
CELERYD_FORCE_EXECV = True  # 防止死锁,应确保为True
CELERY_TASK_TIME_LIMIT = 60 * 30 * 5  # 限制celery任务执行时间，# 单个任务的运行时间限制，否则会被杀死
CELERYD_MAX_TASKS_PER_CHILD = 100  # worker执行100个任务自动销毁，防止内存泄露
CELERYD_TASK_SOFT_TIME_LIMIT = 6000  # 单个任务的运行时间不超过此值(秒)，否则会抛出(SoftTimeLimitExceeded)异常停止任务
CELERY_DISABLE_RATE_LIMITS = True  # 即使任务设置了明确的速率限制，也禁用所有速率限制。
