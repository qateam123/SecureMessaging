from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://localhost:5000/message")
from_input = driver.find_element_by_id("from_input")
from_input.send_keys("gemma.irving@ons.gov.uk")
to_input = driver.find_element_by_id("to_input")
to_input.send_keys("gemma.irving@qa.com")
message_input = driver.find_element_by_id("message_input")
message_input.send_keys("test, test, test")
driver.find_element_by_id("submit").click()
