from selenium import webdriver      
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import time
from simplebrowser import SimpleBrowser
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def module_browser():
    browser = os.getenv('BROWSER', 'chrome')
    logger.info('creating browser %s', browser)
    module_browser = SimpleBrowser(browser=browser)
    module_browser.get('https://www.fylehq.com')
    module_browser.find_by_xpath(xpath="//span[@class='banner-close']", click=True)
    return module_browser

@pytest.fixture
def browser(module_browser):
    module_browser.get('https://www.fylehq.com')
    module_browser.find_by_xpath(xpath="//a[@id='best-expense-video-id']", click=True)
    return module_browser

def submit_getdemo_form(browser, email=None, firstname=None, lastname=None, phone=None, company_size=None, agree=None):
    if email:
        l = browser.find_by_xpath(xpath="//input[@name='email']", click=True)
        l.send_keys(email)
    
    if firstname:
        l = browser.find_by_xpath(xpath="//input[@name='firstname']", click=True)
        l.send_keys(firstname)

    if lastname:
        l = browser.find_by_xpath(xpath="//input[@name='lastname']", click=True)
        l.send_keys(lastname)

    if phone:
        l = browser.find_by_xpath(xpath="//input[@name='phone']", click=True)
        l.send_keys(phone)

    if company_size:
        l = browser.find_by_xpath(xpath="//input[@id='number_of_employees']", click=True)
        l = browser.find_by_xpath(xpath=f"//li[@data-value='{company_size}']", click=True)

    if agree:
        l = browser.find_by_xpath(xpath="//input[@name='gdpr_consent']")
        browser.checkbox_click(l)

    time.sleep(1)
    l = browser.find_by_xpath(xpath='//button[text()="Get a demo"]', click=True)
    time.sleep(4)


def test_bad_email(browser):
    submit_getdemo_form(browser, email='foo')
    e = browser.find_by_xpath(xpath="//label[@for='demo-email'][@class='error']")
    assert e, 'No error displayed for invalid email'

def test_missing_firstname(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in')
    e = browser.find_by_xpath(xpath="//label[@for='demo-first-name'][@class='error demo-first-name-error']")
    assert e, 'No error displayed for missing firstname'

def test_success(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in', firstname='Megatron', lastname='Transformer', phone='123456789', company_size='Under 5', agree=True)
    e = browser.find_by_xpath(xpath="//h3[contains(text(), 'Thank')]")
    assert e and e.is_displayed(), 'Not displaying thank you message'


