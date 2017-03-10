from selenium import webdriver

driver = webdriver.Chrome()

driver.get("http://localhost:5000/new-message")

fromInput = driver.find_element_by_id("from_input")
fromInput.send_keys("mohammad.islam@qa.com")
toInput = driver.find_element_by_id("to_input")
toInput.send_keys("mo")
messageInput = driver.find_element_by_id("message_input")
messageInput.send_keys("test, test, test")
driver.find_element_by_id("submit").click()
