import requests
from behave import *


# Scenario: Ensure message sent to API endpoint

@given('A new message is created')
def step_impl(context):
    context.new_message = {
        "to": "emilio.ward@qa.com",
        "from": "emilio.ward@ons.gov.uk",
        "message": "testing 1, 2, 3"
    }


@when("a request for a new message is submitted")
def step_impl(context):
    message_endpoint = "http://172.28.93.106:5050/message"
    print("The url to go to is: " + message_endpoint)
    headers = {'Content-type': 'application/json'}
    context.response = requests.post(message_endpoint, json=context.new_message, headers=headers)

    assert context.response.status_code == 201
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('the message is created successfully, reached API endpoint')
def step_impl(context):
    pass
