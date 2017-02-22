import unittest
# import os
# import sys
from app import app

from flask import request, redirect, json

class FlaskTestCase(unittest.TestCase):

    def test_username_valid(self):
        tester = app.test_client(self)
        response = tester.get("/validate?username=" + "username", content_type='application/json')
        print(response.data, file=sys.stderr)
        self.assertEqual(json.loads(response.data), {"usernameValid": True})

    def test_username_invalid(self):
        tester = app.test_client(self)
        response = tester.get("/validate?username=" + "username", content_type='application/json')
        print(response.data, file=sys.stderr)
        self.assertEqual(json.loads(response.data), {"usernameValid": False})

if __name__ == '__main__':
  unittest.main()
