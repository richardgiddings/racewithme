#
#   Dev settings
#

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '51o&jjqmi+ig$qp-%b%hvnpe#hf^ef0019zs-59^e_ps(emb5p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"), # project 
]