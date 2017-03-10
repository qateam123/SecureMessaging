from selenium import webdriver

from selenium import webdriver

driver = webdriver.Chrome()

driver.get("http://localhost:5000/new-message")

fromInput = driver.find_element_by_id("from_input")
fromInput.send_keys("mohammad.islam@qa.com")
to = driver.find_element_by_id("to_input")
to.send_keys("mohammad.islam@ons.gov.uk")
driver.find_element_by_id("submit").click()