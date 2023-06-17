from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cafe',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}