# pip install chromedriver-py
from selenium import webdriver
from chromedriver_py import binary_path # This will get you the path variable

svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)

# Deprecated, but it works in older Selenium versions
# driver = webdriver.Chrome(executable_path=binary_path)
driver.get("http://www.python.org") #
assert "Python" in driver.title