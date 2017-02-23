import unittest
#import sys
#sys.path.append('../../SecureMessaging')

from app import app

from flask import json

class FlaskTestCase(unittest.TestCase):

    def test_msg_valid(self):
        tester = app.test_client(self)
        response = tester.get("/validate?msg=" + "msg", content_type='application/json')
        self.assertEqual(json.loads(response.data), {"msgValid": True, 'msg': 'msg'})

    def test_msg_invalid(self):
        tester = app.test_client(self)
        response = tester.get("/validate?msg=", content_type='application/json')
        self.assertEqual(json.loads(response.data), {"msgValid": False, 'msg': 'empty'})

if __name__ == '__main__':
  unittest.main()
