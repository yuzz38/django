ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:8000',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []
CORS_ALLOW_CREDENTIALS = True 
DEBUG = True

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}