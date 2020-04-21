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
    module_browser.input(xpath="//span[@class='banner-close']", click=True)
    return module_browser
    # yield module_browser
    # del module_browser

@pytest.fixture
def browser(module_browser):
    module_browser.get('https://www.fylehq.com')
    module_browser.input(xpath="//a[@id='best-expense-video-id']", click=True)
    return module_browser

def submit_getdemo_form(browser, email=None, firstname=None, lastname=None, phone=None, company_size=None, agree=None):
    if email:
        browser.input(xpath="//input[@name='email']", keys=email)
    if firstname:
        browser.input(xpath="//input[@name='firstname']", keys=firstname)
    if lastname:
        browser.input(xpath="//input[@name='lastname']", keys=lastname)
    if phone:
        browser.input(xpath="//input[@name='phone']", keys=phone)
    if company_size:
        browser.input(xpath="//input[@id='number_of_employees']", click=True)
        browser.input(xpath=f"//li[@data-value='{company_size}']", click=True)
    if agree:
        browser.input(xpath="//input[@name='gdpr_consent']", click=True)
    time.sleep(1)
    browser.input(xpath='//button[text()="Get a demo"]', click=True)
    time.sleep(2)


def test_bad_email(browser):
    submit_getdemo_form(browser, email='foo')
    e = browser.find(xpath="//label[@for='demo-email'][@class='error']")
    assert e and e.is_displayed(), 'No error displayed for invalid email'

def test_missing_firstname(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in')
    e = browser.find(xpath="//label[@for='demo-first-name'][@class='error demo-first-name-error']")
    assert e and e.is_displayed(), 'No error displayed for missing firstname'

def test_success(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in', firstname='Megatron', lastname='Transformer', phone='123456789', company_size='Under 5', agree=True)
    e = browser.find(xpath="//h3[contains(text(), 'Thank')]")
    assert e and e.is_displayed(), 'Not displaying thank you message'


