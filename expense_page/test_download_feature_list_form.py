import time
import logging
import pytest
from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    time.sleep(0.5)
    module_browser.get(base_url + "/expense-management")
    module_browser.find(xpath="//section[contains(@class, 'download-feature-list-section')]", scroll=True)
    module_browser.click(xpath="//button[contains(@class, 'feature-list-download-btn')]")
    time.sleep(1)
    return module_browser

def submit_getdemo_form(browser, email=None, firstname=None, lastname=None, phone=None, company_size=None, agree=None):
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
        browser.click(xpath=f"//div[contains(@class, 'compare-feature-body')]//li[@data-value='{company_size}']")
    if agree:
        browser.click(xpath="//div[contains(@class, 'compare-feature-body')]//div[contains(@class, 'custom-checkbox')]")
    browser.click(xpath="//div[contains(@class, 'compare-feature-body')]//button[text()='Download']")

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email(browser):
    submit_getdemo_form(browser, email='foo')
    e = browser.find(xpath="//div[contains(@class, 'compare-feature-body')]//label[@for='demo-email-feature-download'][@class='error']")
    assert e and e.is_displayed(), 'No error displayed for invalid email'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_missing_firstname(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in')
    e = browser.find(xpath="//div[contains(@class, 'compare-feature-body')]//label[@for='demo-first-name-feature-download'][@class='error demo-first-name-error']")
    assert e and e.is_displayed(), 'No error displayed for missing firstname'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in', firstname='Megatron', lastname='Transformer', phone='123456789', company_size='Under 5', agree=True)
    time.sleep(2)
    e = browser.find(xpath="//h3[contains(text(), 'Thank')]")
    assert e and e.is_displayed(), 'Not displaying thank you message'

