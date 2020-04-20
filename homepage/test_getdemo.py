from selenium import webdriver      
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import time
from browser import Browser
import logging
import pytest

@pytest.fixture
def browser():
    browser = os.getenv('BROWSER', 'chrome')
    b = Browser(browser=browser)
    b.get('https://www.fylehq.com')
    b.find_by_xpath(xpath="//span[@class='banner-close']", click=True)
    b.find_by_xpath(xpath="//a[@id='best-expense-video-id']", click=True)
    return b

def submit_getdemo_form(browser, email=None, firstname=None, lastname=None, phone=None, company_size=None, agree=None):
    if email:
        l = browser.find_by_xpath(xpath="//input[@name='email']")
        l.send_keys(email)
    
    if firstname:
        l = browser.find_by_xpath(xpath="//input[@name='firstname']")
        l.send_keys(firstname)

    if lastname:
        l = browser.find_by_xpath(xpath="//input[@name='lastname']")
        l.send_keys(lastname)

    if phone:
        l = browser.find_by_xpath(xpath="//input[@name='phone']")
        l.send_keys(phone)

    if company_size:
        l = browser.find_by_css_selector(css_selector='div.form-employees', click=True)
        l = browser.find_by_xpath(xpath=f"//li[@data-value='{company_size}']", click=True)

    if agree:
        l = browser.find_by_css_selector(css_selector='div.custom-checkbox', click=True)
        l.click()

    l = browser.find_by_xpath(xpath='//button[text()="Get a demo"]', click=True)


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
    assert e, 'Thank you not displayed'


