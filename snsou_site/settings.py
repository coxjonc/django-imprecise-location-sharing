"""
Django settings for Sun Never Sets on Us project.
Copyright 2015 Jonathan Cox
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '.sunneversetson.us', 
    '.herokuapp.com', 
    '.google.com',
    'chrome-extension://mingiamebfhmhfdgapghhplefcpedohl',
    'chrome-extension://hohebpomhmfngamgpmmlchgilecfejgb'
]

# Application definitions

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'neversets',
    'corsheaders',
    'friendship',
    'allauth',
    'allauth.account',
    'allauth.socialaccount'
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'snsou_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates', 'account')],
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
#---------
#DATABASES
#---------

import dj_database_url
DATABASES = {}
DATABASES['default'] = dj_database_url.config()
#Enable persistent connections
DATABASES['default']['CONN_MAX_AGE'] = 500

#--------------------
#INTERNATIONALIZATION
#--------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#-------
#LOGGING
#-------
LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}


#------------
#EMAIL CONFIG 
#------------

DEFAULT_FROM_EMAIL='jonathan@sunneversetson.us'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PW']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#--------------------------------------
#STATIC FILES (CSS, JavaScript, Images)
#--------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = 'staticfiles'

STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


WSGI_APPLICATION = 'snsou_site.wsgi.application'

#Allow CORS requests from any domain
CORS_ORIGIN_WHITELIST = (
    'chrome-extension://mingiamebfhmhfdgapghhplefcpedohl',
    'chrome-extension://hohebpomhmfngamgpmmlchgilecfejgb'
)
#Allow CORS requests from other domains to set headers
#Necessary for Chrome extensions to specify how form is encoded 
CORS_ALLOW_CREDENTIALS = True

#------------------------
#AUTHENTICATION
#------------------------

#Use custom user model

AUTH_USER_MODEL = 'neversets.UserProfile'

#AllAuth settings

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_FORM_CLASS = 'neversets.forms.SignupForm'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/signup/'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

LOGIN_REDIRECT_URL = "/profile/"

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)
