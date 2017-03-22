import os

SECURE_MESSAGING_API_URL = os.getenv('SECURE_MESSAGING_API_URL', "http://localhost:5050/message")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MAX_CHARS = 1200
