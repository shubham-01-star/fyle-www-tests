from selenium import webdriver      
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException
import os
import time
import logging

logger = logging.getLogger(__name__)

class SimpleBrowser:

    @classmethod
    def __create_driver(cls, browser='chrome'):
        assert browser in ['chrome', 'safari', 'firefox', None], 'unsupported browser'
        driver = None
        for i in range(0, 3):
            try:
                if browser == 'safari':
                    driver = webdriver.Safari()
                if browser == 'chrome' or not browser:
                    driver = webdriver.Chrome()
            except SessionNotCreatedException as e:
                logger.error('couldnt create session properly')
                time.sleep(4)
            if driver:
                break
        return driver

    def __init__(self, browser='chrome'):
        self.browser = browser
        self.driver = SimpleBrowser.__create_driver(browser=browser)
        assert self.driver, 'unable to initialize browser properly'
        self.timeout = 5
        self.wait = WebDriverWait(self.driver, self.timeout)

    def close(self):
        logger.info('shutting down driver')
        time.sleep(1)
        driver = self.driver
        self.driver = None
        if not driver:
            driver.close()
        time.sleep(2)

    def __del__(self):
        self.close()

    def get(self, url):
        return self.driver.get(url)

    def checkbox_click(self, elem):
        self.driver.execute_script("arguments[0].click();", elem)

    def find(self, xpath):
        l = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return l

    def input(self, xpath, keys=None, click=False):
        assert (keys and not click) or (not keys and click), 'only one of keys or click actions can be performed'
        l = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        assert l.tag_name in ['input', 'li', 'button', 'span', 'a'], 'xpath did not return proper element'
        if click:
            if l.get_attribute('type') == 'checkbox':
                # strange issue where checkbox click isnt working properly in safari
                self.driver.execute_script("arguments[0].click();", l)
            else:
                l = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                l.click()
        if keys:
            l = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            l.send_keys(keys)
        return l

    def mark_divs(self, browser):
        for d in self.driver.find_elements_by_xpath("//div"):
            self.driver.execute_script("arguments[0]['style']['border']='1px solid black';", d)

