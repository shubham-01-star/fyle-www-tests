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
    b = Browser()
    b.get('https://www.fylehq.com')
    b.find_by_xpath("//a[@id='best-expense-video-id']").click()
    return b

def submit_getdemo_form(browser, email=None, firstname=None, lastname=None, phone=None, company_size=None, agree=None):
    if email:
        l = browser.find_by_xpath("//input[@name='email']")
        l.send_keys(email)
    
    if firstname:
        l = browser.find_by_xpath("//input[@name='firstname']")
        l.send_keys(firstname)

    if lastname:
        l = browser.find_by_xpath("//input[@name='lastname']")
        l.send_keys(lastname)

    if phone:
        l = browser.find_by_xpath("//input[@name='phone']")
        l.send_keys(phone)

    if company_size:
        l = browser.find_by_css_selector('div.form-employees')    
        l.click()
        l = browser.find_by_xpath(f"//li[@data-value='{company_size}']")
        l.click()

    if agree:
        l = browser.find_by_css_selector('div.custom-checkbox')    
        l.click()

    l = browser.find_by_xpath('//button[text()="Get a demo"]')
    l.click()


def test_bad_email(browser):
    submit_getdemo_form(browser, email='foo')
    e = browser.find_by_xpath("//label[@for='demo-email'][@class='error']")
    assert e, 'No error displayed for invalid email'

def test_missing_firstname(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in')
    e = browser.find_by_xpath("//label[@for='demo-first-name'][@class='error demo-first-name-error']")
    assert e, 'No error displayed for missing firstname'

def test_success(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in', firstname='Megatron', lastname='Transformer', phone='123456789', company_size='Under 5', agree=True)
    e = browser.find_by_xpath("//h3[contains(text(), 'Thank')]")
    assert e, 'Thank you not displayed'


