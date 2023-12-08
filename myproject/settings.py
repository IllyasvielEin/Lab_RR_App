import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'abc123'

DEBUG = True

# WSGI_APPLICATION = 'labapp.wsgi.application'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'labapp.apps.LabAppConfig',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sci',  # 数据库名称
        'USER': 'sci',  # 数据库用户名
        'PASSWORD': 'sci',  # 数据库密码
        'HOST': '192.168.6.226',  # 数据库主机，例如 '127.0.0.1' 或 'localhost'
        'PORT': '3306',  # MySQL 默认端口号为 3306
    }
}

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

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'labapp/static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Harbin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logger
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 基本配置，可以复用的
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # 禁用已经存在的logger实例
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {  # 定义了两种日志格式
        "verbose": {  # 详细
            "format": "%(levelname)s %(asctime)s [%(module)s]: "
                      "%(message)s"
        },
        'simple': {  # 简单
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
    },
    "handlers": {  # 定义了三种日志处理方式
        "mail_admins": {  # 只有debug=False且Error级别以上发邮件给admin
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        'file': {  # 对WARNING级别以上信息以日志文件形式保存
            'level': "WARNING",
            'class': 'logging.handlers.RotatingFileHandler',  # 滚动生成日志，切割
            'filename': os.path.join(LOG_DIR, 'django.log'),  # 日志文件名
            'maxBytes': 1024 * 1024 * 10,  # 单个日志文件最大为10M
            'backupCount': 5,  # 日志备份文件最大数量
            'formatter': 'simple',  # 简单格式
            'encoding': 'utf-8',  # 放置中文乱码
        },
        "console": {  # 打印到终端console
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },

    "loggers": {
        "labapp": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,  # 向不向更高级别的logger传递
        }
    },
}
