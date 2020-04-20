from selenium import webdriver      
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import os
import time
import logging

logger = logging.getLogger(__name__)

class Browser:
    def __init__(self, browser='chrome'):
        self.driver = webdriver.Chrome()
        self.timeout = 5
        self.wait = WebDriverWait(self.driver, self.timeout)

    # def __del__(self):
    #     time.sleep(5)
    #       self.driver.close()

    def get(self, url):
        return self.driver.get(url)

    # TODO: try to make it more generic
    def find_by_xpath(self, xpath):
        l = None
        try:
            l = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException as e:
            logger.error('timeout while searching for element in %s', xpath)
        return l

    def find_by_css_selector(self, css_selector):
        l = None
        try:
            l = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        except TimeoutException as e:
            logger.error('timeout while searching for element in %s', xpath)
        return l

    # def find_elem_by_xpath(self, xpath):
    #     l = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #     return l

    def mark_divs(self, browser):
        for d in self.driver.find_elements_by_xpath("//div"):
            self.driver.execute_script("arguments[0]['style']['border']='1px solid black';", d)

    def close(self):
        self.driver.close()
