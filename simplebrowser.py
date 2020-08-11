import logging
import random
from time import sleep
import json

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class SimpleBrowser:

    @classmethod
    def __create_chrome_driver(cls, width, height):
        assert width
        assert height
        options = Options()
        options.add_argument(f'--window-size={width},{height}')
        driver = webdriver.Chrome(options=options)
        return driver

    @classmethod
    def __create_safari_driver(cls, width, height):
        driver = webdriver.Safari()
        driver.set_window_size(width, height)
        return driver

    @classmethod
    def __create_driver(cls, browser, width, height):
        assert browser in ['chrome', 'safari',
                           'firefox', None], 'unsupported browser'
        driver = None
        for _ in range(0, 3):
            try:
                if browser == 'safari':
                    driver = SimpleBrowser.__create_safari_driver(
                        width=width, height=height)
                if browser == 'chrome' or not browser:
                    driver = SimpleBrowser.__create_chrome_driver(
                        width=width, height=height)
            except SessionNotCreatedException:
                logger.exception('couldnt create session properly')
                sleep(4)
            if driver:
                break
        return driver

    def __init__(self, browser, width, height):
        self.browser = browser
        self.driver = SimpleBrowser.__create_driver(
            browser=browser, width=width, height=height)
        assert self.driver, 'unable to initialize browser properly'
        self.timeout = 5
        self.wait = WebDriverWait(self.driver, self.timeout)

    def close(self):
        sleep(1)
        driver = self.driver
        self.driver = None
        if driver:
            driver.close()
        sleep(2)

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

    def scroll_down_page(self, max_speed=300):
        current_scroll_position = 0
        new_height = 1
        while current_scroll_position <= new_height:
            delta = random.randint(1, max_speed)
            current_scroll_position += delta
            self.driver.execute_script(f'window.scrollTo(0, {current_scroll_position});')
            sleep(random.uniform(0.0, 1.0))
            new_height = self.current_height()

    def scroll_up_page(self, max_speed=300):
        pos = self.current_scroll_position()
        while pos > 0:
            delta = random.randint(1, max_speed)
            pos -= delta
            if pos < 0:
                pos = 0
            self.driver.execute_script(f'window.scrollTo(0, {pos});')
            sleep(random.uniform(0.0, 1.0))

    def scroll_down(self, pixels_to_scroll):
        self.driver.execute_script(f'window.scrollBy(0, {pixels_to_scroll});')
        sleep(random.uniform(0.0, 1.0))

    def find(self, xpath, scroll=False):
        try:
            l = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", l)
                sleep(1)
                l = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            l = False
        return l

    def find_many(self, xpath):
        m = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return m

    def click(self, xpath, scroll=False):
        l = self.find(xpath, scroll)
        # if self.is_mobile():
        #     self.scroll_down(80)
        sleep(2)
        ltag = l.tag_name.lower() if l.tag_name else None
        assert ltag in ['input', 'li', 'button', 'span',
                        'a', 'div', 'textarea'], 'xpath did not return proper element'
        l = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        l.click()
        sleep(3)
        return l
    
    def click_element(self, element):        
        element.click()
        sleep(3)
        return element

    def input(self, xpath, keys, scroll=False):
        l = self.find(xpath, scroll)
        ltag = l.tag_name.lower() if l.tag_name else None
        # logger.info('found element with tag %s', ltag)
        assert ltag in ['input', 'li', 'button', 'span',
                        'a', 'div', 'textarea'], 'xpath did not return proper element'
        l = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        l.click()
        sleep(0.1)
        l.send_keys(keys)
        sleep(0.1)
        return l

    def close_windows(self):
        # close all windows except 0
        while len(self.driver.window_handles) > 1:
            w = self.driver.window_handles[-1]
            self.driver.switch_to.window(w)
            self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def mark_divs(self):
        for d in self.driver.find_elements_by_xpath("//div"):
            self.driver.execute_script(
                "arguments[0]['style']['border']='1px solid black';", d)

    def get_width(self):
        return self.driver.get_window_size()['width']

    def get_height(self):
        return self.driver.get_window_size()['height']

    def is_desktop(self):
        return self.get_width() >= 1024

    def is_mobile(self):
        return self.get_width() < 425

    def is_tablet(self):
        return self.get_width() >= 425 and self.get_width() < 1024

    def get_current_url(self):
        return self.driver.current_url

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)

    def check_horizontal_overflow(self):
        return self.driver.execute_script("return document.documentElement.scrollWidth>document.documentElement.clientWidth")

    def hover(self, elem):
        ltag = elem.tag_name.lower() if elem.tag_name else None
        assert ltag in ['li', 'button', 'span',
                        'a', 'div'], 'xpath did not return proper element'
        actions = ActionChains(self.driver)
        actions.move_to_element(elem)
        actions.perform()
        return elem

    def refresh(self):
        return self.driver.refresh()

    def back(self):
        return self.driver.back()

    def switch_tab_next(self, number):
        return self.driver.switch_to.window(self.driver.window_handles[number])

    # method to get the downloaded file name
    def get_downLoadeded_filename(self):
        self.driver.execute_script("window.open()")
        # switch to new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # navigate to chrome downloads
        self.driver.get('chrome://downloads')
        return self.driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').href")

    def get_from_local_storage(self, key):
        return json.loads(self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key))

    def set_local_storage(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def clear_local_storage(self):
        self.driver.execute_script("window.localStorage.clear();")
