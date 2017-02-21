import unittest
import os
import sys
#from app.views import views
from app.views import views
#from .app import app

from flask import request

class FlaskTestCase(unittest.TestCase):

    def test_username_valid():
        response = redirect("/validate?username=" + "username")
        assertEqual(json.loads(response.data), {"username": True})

    def test_username_invalid():
        response = redirect("/validate?username=")
        assertEqual(json.loads(response.data), {"username": False})

if __name__ == '__main__':
  unittest.main()
