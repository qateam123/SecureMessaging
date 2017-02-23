import unittest
#import sys
#sys.path.append('../../SecureMessaging')

from app import app

from flask import json

class FlaskTestCase(unittest.TestCase):

    def test_username_valid(self):
        tester = app.test_client(self)
        response = tester.get("/validate?username=" + "username", content_type='application/json')
        self.assertEqual(json.loads(response.data), {"usernameValid": True})

    def test_username_invalid(self):
        tester = app.test_client(self)
        response = tester.get("/validate?username=", content_type='application/json')
        self.assertEqual(json.loads(response.data), {"usernameValid": False})

if __name__ == '__main__':
  unittest.main()
