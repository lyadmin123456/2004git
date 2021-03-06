"""
Django settings for edu_api2 project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import datetime
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 修改默认的子应用的目录后，需要将apps的目录设置为全局的导包路径
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret keys used in production secret!
SECRET_KEY = '=a&%7w$g+lgxhgl@1qk)2&w0tdkl@f!6d1n*a_glk0&m&q^d2g'

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
    'rest_framework',
    'corsheaders',
    'xadmin',
    'crispy_forms',
    'reversion',
# 富文本编辑器配置
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器的上传模块

    'edu_api2.apps.home',
    'edu_api2.apps.user',
    'edu_api2.apps.course',
    'edu_api2.apps.cart',
    'edu_api2.apps.payments',
    'edu_api2.apps.order',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edu_api2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'edu_api2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/


LANGUAGE_CODE = 'zh_Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ =False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# 静态资源配置
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 日志配置
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已存在的日志器
    'disable_existing_loggers': False,
    # 格式化日志信息
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # 日志的过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理日志的方法
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            # 记录到文件中的日志级别
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件的位置  日志的文件名  日志的文职
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/lesson_api.log"),
            # 日志文件的大小  100M
            'maxBytes': 100 * 1024 * 1024,
            # 日志文件的最大数量
            'backupCount': 10,
            # 记录到文件的日志格式
            'formatter': 'verbose'
        },
    },
    # 日志对象
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}
# 跨域问题
CORS_ORIGIN_ALLOW_ALL = True
# 全局异常配置
REST_FRAMEWORK = {
    # 默认的全局异常的处理方法
    # 'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'EXCEPTION_HANDLER': 'edu_api2.utils.exceptions.exception_handler',  # 使用自定义异常

    #    认证配置

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ]
}
# 注册用户模型
AUTH_USER_MODEL = 'user.UserInfo'

# Token有效时间
JWT_AUTH = {
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(seconds=30000000),
    #     自定义jwt登陆返回值
    "JWT_RESPONSE_PAYLOAD_HANDLER": "user.utils.jwt_response_payload_handler",
}
# 修改默认登录
AUTHENTICATION_BACKENDS = [
    'edu_api2.apps.user.utils.UserAuth',
]
# django-redis配置
CACHES = {
    # 默认库
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接的redis所在服务的端口以及ip
        "LOCATION": "redis://127.0.0.1:6379/0",
        # 使用客户端的方式
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

    # 验证码储存位置
    "msg_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接的redis所在服务的端口以及ip
        "LOCATION": "redis://127.0.0.1:6379/10",
        # 使用客户端的方式
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 购物车的储存位置
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接的redis所在服务的端口以及ip
        "LOCATION": "redis://127.0.0.1:6379/9",
        # 使用客户端的方式
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
# 使用drf的静态资源配置
CKEDITOR_UPLOAD_PATH = ""

# ckeditor相关配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        # 'width': 300,
    },
}
# 支付宝支付链接的生成
ALIAPY_CONFIG = {
    # "gateway_url": "https://openapi.alipay.com/gateway.do?", # 真实支付宝网关地址
    "gateway_url": "https://openapi.alipaydev.com/gateway.do?",  # 沙箱支付宝网关地址
    "appid": "2016102700769510",
    "app_notify_url": None,
    "app_private_key_path": open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read(),
    "alipay_public_key_path": open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read(),
    "sign_type": "RSA2",
    "debug": False,
    # "return_url": "http://www.baizhistore.cn:8080/payments/result",  # 同步回调地址
    "return_url": "http://localhost:8080/ordersuccess",  # 同步回调地址
    "notify_url": "http://127.0.0.1:8000/payments/result",  # 异步结果通知
}



