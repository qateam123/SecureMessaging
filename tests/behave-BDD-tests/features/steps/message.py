from behave import *
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://localhost:5000/new-message")
# Scenario: Ensure message sent to API endpoint

@given('A new message is created')
def step_impl(context):
    from_input = driver.find_element_by_id("from_input")
    from_input.send_keys("gemma.irving@ons.gov.uk")
    to_input = driver.find_element_by_id("to_input")
    to_input.send_keys("gemma.irving@qa.com")
    message_input = driver.find_element_by_id("message_input")
    message_input.send_keys("test, test, test")

@when("a request for a new message is submitted")
def step_impl(context):
    driver.find_element_by_id("submit").click()

@then("Successful response from API")
def step_impl(context):
    driver.find_element_by_id("bubbles")
    pass
