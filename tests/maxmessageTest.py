from selenium import webdriver

driver = webdriver.Chrome()

driver.get("http://localhost:5000/new-message")

fromInput = driver.find_element_by_id("from_input")
fromInput.send_keys("mohammad.islam@qa.com")
toInput = driver.find_element_by_id("to_input")
toInput.send_keys("mohammad.islam@ons.gov.uk")
messageInput = driver.find_element_by_id("message_input")
messageInput.send_keys("test, test, test, test, test, test, test, test, test, test, test, test, test, test, test, test, test, test, whueifewiwdfioewjiofewiohfioewuoghrighiorheighiewhgiorehioghioehwqgiohriowhgiohrqoighioehgiohriohgrhehgierohgoirheguhreuhghrwqioGHIOWASHIOGHIDOSAKIOGHDIASOGIOHAISGHIOSDIOGHIOSDHIOGDHISOAGHDOSDHGHDOSAGODSAGODSAGHOHFODSHOFHDOGHODSAHODHGODSAHGDOHOHGOAGODSOHFDHFHDJSAHGIDSAHGIDSAGODASGIODHIDGHIIDWHIOIGOHDIOAHGIODHGIOAHGDOVUNDUIEWWGYRRDKOSLewarsdtfyuiop0[iuytfyuiop[oiuytrdyuiop0iuytfuio0p[iuytryuop0tyryop0ytryop[oiuuiop'oidfop['odsop[;\dsziop'dfsz;'[ljhgfh;'lkjhgfjkl;'|:lkjhl;'\];lkjhgflp;fdszf']\;lgfdszfgl;['lpgfdxgo;lp[\];poiyuiop0[=]poiuytrestyuiop[]poiuydsuiop[]diogiojeiiewgiorewjgiojrewogjiorewjgoirejwgioreigwigojriewojgiroejgifedos")
driver.find_element_by_id("submit").click()
