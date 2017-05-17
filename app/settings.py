import os

SECURE_MESSAGING_API_URL = os.getenv('SECURE_MESSAGING_API_URL', "http://localhost:5050/")
SM_SEND_MESSAGE_URL = "message/send"
SM_GET_MESSAGES_URL = "messages"
SM_GET_MESSAGE_URL = "message/{0}"
SM_MODIFY_MESSAGE_URL = "message/{0}/modify"
SM_SAVE_DRAFT_URL = "draft/save"
SM_MODIFY_DRAFT_URL = "draft/{0}/modify"
SM_GET_DRAFT_URL = "draft/{0}"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MAX_CHARS = 1200

JWT_SECRET = os.getenv('JWT_SECRET', 'vrwgLNWEffe45thh545yuby')

#  Keys
SM_USER_AUTHENTICATION_PRIVATE_KEY = open("{0}/jwt-test-keys/sm-user-authentication-encryption-private-key.pem".format(os.getenv('RAS_SM_PATH'))).read()
SM_USER_AUTHENTICATION_PUBLIC_KEY = open("{0}/jwt-test-keys/sm-user-authentication-encryption-public-key.pem".format(os.getenv('RAS_SM_PATH'))).read()

#  password
SM_USER_AUTHENTICATION_PRIVATE_KEY_PASSWORD = "digitaleq"
