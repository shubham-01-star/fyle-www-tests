from time import sleep
import logging

logger = logging.getLogger(__name__)

def open_download_feature_form(browser):
    browser.find(xpath="//section[contains(@class, 'download-feature-list-section')]", scroll=True)
    browser.click(xpath="//button[contains(@class, 'feature-list-download-btn')]")
    sleep(1)

def submit_download_feature_form(browser, email=None, firstname=None, lastname=None, phone=None, company_size=None, agree=None):
    if email:
        browser.input(xpath="//div[contains(@class, 'compare-feature-body')]//input[@name='email']", keys=email)
    if firstname:
        browser.input(xpath="//div[contains(@class, 'compare-feature-body')]//input[@name='firstname']", keys=firstname)
    if lastname:
        browser.input(xpath="//div[contains(@class, 'compare-feature-body')]//input[@name='lastname']", keys=lastname)
    if phone:
        browser.input(xpath="//div[contains(@class, 'compare-feature-body')]//input[@name='phone']", keys=phone)
    if company_size:
        browser.click(xpath="//div[contains(@class, 'compare-feature-body')]//input[@id='number_of_employees-feature-download']")
        browser.click(xpath=f"//div[contains(@class, 'compare-feature-body')]//li[@value='{company_size}']")
    if agree:
        browser.click(xpath="//div[contains(@class, 'compare-feature-body')]//div[contains(@class, 'custom-checkbox')]")
    browser.click(xpath="//div[contains(@class, 'compare-feature-body')]//button[text()=' Download ']")

def assert_bad_email_download_feature_form(browser):
    open_download_feature_form(browser)
    submit_download_feature_form(browser, email='foo')
    e = browser.find(xpath="//div[contains(@class, 'compare-feature-body')]//label[@for='demo-email-feature-download'][@class='error']")
    assert e and e.is_displayed(), 'No error displayed for invalid email'

def assert_missing_firstname_download_feature_form(browser):
    open_download_feature_form(browser)
    submit_download_feature_form(browser, email='test@fyle.in')
    e = browser.find(xpath="//div[contains(@class, 'compare-feature-body')]//label[@for='demo-first-name-feature-download'][@class='error demo-first-name-error']")
    assert e and e.is_displayed(), 'No error displayed for missing firstname'

def assert_success_download_feature_form(browser):
    open_download_feature_form(browser)
    submit_download_feature_form(browser, email='test@fyle.in', firstname='test', lastname='test', phone='123456789', company_size='Under 5', agree=True)
    sleep(2)
    e = browser.find(xpath="//h3[contains(text(), 'Thank')]")
    assert e and e.is_displayed(), 'Not displaying thank you message'
