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

class Browser:
    def __init__(self, browser='chrome'):
        assert browser in ['chrome', 'safari', 'firefox', None], 'unsupported browser'
        self.driver = None

        for i in range(0, 3):
            try:
                if browser == 'safari':
                    self.driver = webdriver.Safari()
                if browser == 'chrome' or not browser:
                    self.driver = webdriver.Chrome()
            except SessionNotCreatedException as e:
                logger.error('couldnt create session properly')
                time.sleep(4)
            if self.driver:
                break

        assert self.driver, 'unable to initialize browser properly'
        self.timeout = 5
        self.wait = WebDriverWait(self.driver, self.timeout)

    def close(self):
        logger.debug('shutting down driver')
        self.driver.close()
        time.sleep(4)

    def __del__(self):
        self.close()

    def get(self, url):
        return self.driver.get(url)

    def find_by_xpath(self, xpath, click=False):
        l = None
        try:
            l = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            # TODO: this is a hack - needs to be removed somehow
            if click == True:
                self.driver.execute_script("arguments[0].click();", l)

        except TimeoutException as e:
            logger.error('timeout while searching for element in %s', xpath)
            
        return l

    def find_by_css_selector(self, css_selector, click=False):
        l = None
        try:
            l = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            # TODO: this is a hack - needs to be removed somehow
            if click == True:
                self.driver.execute_script("arguments[0].click();", l)
        except TimeoutException as e:
            logger.error('timeout while searching for element in %s', css_selector)
        return l

    # def find_elem_by_xpath(self, xpath):
    #     l = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #     return l

    def mark_divs(self, browser):
        for d in self.driver.find_elements_by_xpath("//div"):
            self.driver.execute_script("arguments[0]['style']['border']='1px solid black';", d)

