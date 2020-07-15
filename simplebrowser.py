from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
import os
import time
import logging
import random

logger = logging.getLogger(__name__)


class SimpleBrowser:

    @classmethod
    def __create_chrome_driver(cls, device):
        options = Options()
        if device == 'nexus':
            mobile_emulation = {
                "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
            options.add_experimental_option(
                "mobileEmulation", mobile_emulation)
        else:
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        return driver

    @classmethod
    def __create_safari_driver(cls, device):
        driver = webdriver.Safari()
        driver.set_window_size(1920, 1080)
        return driver

    @classmethod
    def __create_driver(cls, browser, device):
        assert browser in ['chrome', 'safari',
                           'firefox', None], 'unsupported browser'
        assert device in ['nexus', None], 'unsupported device'
        driver = None
        for i in range(0, 3):
            try:
                if browser == 'safari':
                    driver = SimpleBrowser.__create_safari_driver(
                        device=device)
                if browser == 'chrome' or not browser:
                    driver = SimpleBrowser.__create_chrome_driver(
                        device=device)
            except SessionNotCreatedException as e:
                logger.exception('couldnt create session properly')
                time.sleep(4)
            if driver:
                break
        return driver

    def __init__(self, browser='chrome', device=None):
        self.browser = browser
        self.driver = SimpleBrowser.__create_driver(
            browser=browser, device=device)
        assert self.driver, 'unable to initialize browser properly'
        self.timeout = 5
        self.wait = WebDriverWait(self.driver, self.timeout)

    def close(self):
        time.sleep(1)
        driver = self.driver
        self.driver = None
        if driver:
            driver.close()
        time.sleep(2)

    def __del__(self):
        logger.debug('destructor called')
        self.close()

    def get(self, url):
        return self.driver.get(url)

    def checkbox_click(self, elem):
        self.driver.execute_script("arguments[0].click();", elem)

    def current_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")

    def current_scroll_position(self):
        return self.driver.execute_script("return window.pageYOffset")

    def scroll_down_page(self, max_speed=200):
        current_scroll_position, new_height= 0, 1
        while current_scroll_position <= new_height:
            delta = random.randint(1, max_speed)
            current_scroll_position += delta
            self.driver.execute_script(f'window.scrollTo(0, {current_scroll_position});')
            time.sleep(random.uniform(0.0, 1.0))
            new_height = self.current_height()

    def scroll_up_page(self, max_speed=200):
        pos = self.current_scroll_position()
        while pos > 0:
            delta = random.randint(1, max_speed)
            pos -= delta
            if pos < 0:
                pos = 0
            self.driver.execute_script(f'window.scrollTo(0, {pos});')
            time.sleep(random.uniform(0.0, 1.0))
 
    def find(self, xpath, scroll=False):
        l = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        if scroll:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", l)
            time.sleep(1)
            l = self.wait.until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        return l

    def find_many(self, xpath):
        m = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return m

    def input(self, xpath, keys=None, click=False, scroll=False):
        assert (keys and not click) or (
            not keys and click), 'only one of keys or click actions can be performed'
        l = self.find(xpath, scroll)
        ltag = l.tag_name.lower() if l.tag_name else None
        ltype = l.get_attribute('type').lower(
        ) if l.get_attribute('type') else None
        # logger.info('found element with tag %s', ltag)
        assert ltag in ['input', 'li', 'button', 'span',
                        'a', 'div', 'textarea'], 'xpath did not return proper element'
        if click:
            # TODO: under certain conditions, we need to resort to JS click. this is not ideal. someday we should fix this
            # - siva
            jsclick = (ltype == 'checkbox' or ltag == 'li')
            if jsclick:
                self.driver.execute_script("arguments[0].click();", l)
                time.sleep(0.5)
            else:
                l = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath)))
                l.click()
        if keys:
            l = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            l.send_keys(keys)
        return l

    def mark_divs(self, browser):
        for d in self.driver.find_elements_by_xpath("//div"):
            self.driver.execute_script(
                "arguments[0]['style']['border']='1px solid black';", d)
