import time
import logging
import pytest
from common.utils import resize_browser
from common.asserts import assert_content_download_thank_you_page
from common.forms import submit_content_download_form

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    time.sleep(0.5)
    module_browser.get(base_url + '/resources/webinars/good-travel-management-partnership-fyle')
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_content_download_inline_form(browser):
    download_form = browser.find(xpath="//form[contains(@id, 'content-download-form')]")
    assert download_form.is_displayed(), "inline form is not present"
    h3_head = browser.find(xpath="//h3[contains(@id, 'report-heading')]")
    assert h3_head and h3_head.is_displayed(), "Form h3 heading is not displayed"
    sub_text = browser.find(xpath="//p[contains(@id, 'report-subtext')]")
    assert sub_text and sub_text.is_displayed(), "Form sub-heading is not displayed"

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_required_fields(browser):
    submit_content_download_form(browser)
    email_error = browser.find(xpath="//label[@for='content-download-form-email'][@class='error']")
    firstname_error = browser.find(xpath="//label[@for='content-download-form-first-name'][@class='error']")
    lastname_error = browser.find(xpath="//label[@for='content-download-form-last-name'][@class='error']")
    company_size_error = browser.find(xpath="//form[contains(@id, 'content-download-form')]//label[@for='number_of_employees'][@class='error']")
    consent_error = browser.find(xpath="//form[contains(@id, 'content-download-form')]//label[@for='gdpr_consent'][@class='error']")
    assert email_error and email_error.is_displayed(), "No error displayed for missing email"
    assert firstname_error and firstname_error.is_displayed(), "No error displayed for missing firstname"
    assert lastname_error and lastname_error.is_displayed(), "No error displayed for missing lastname"
    assert company_size_error and company_size_error.is_displayed(), "No error displayed for missing company size"
    assert consent_error and consent_error.is_displayed(), "No error displayed for missing checkbox"

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_invalid_names(browser):
    submit_content_download_form(browser, firstname='test1', lastname='test2')
    firstname_error = browser.find(xpath="//label[@for='content-download-form-first-name'][@class='error']")
    lastname_error = browser.find(xpath="//label[@for='content-download-form-last-name'][@class='error']")
    assert firstname_error and firstname_error.is_displayed(), "No error displayed for invalid firstname"
    assert lastname_error and lastname_error.is_displayed(), "No error displayed for invalid lastname"

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email(browser):
    submit_content_download_form(browser, email='test')
    email_error = browser.find(xpath="//label[@for='content-download-form-email'][@class='error']")
    assert email_error and email_error.is_displayed(), 'No error displayed for invalid email'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_non_business_email(browser):
    submit_content_download_form(browser, email='test@gmail.com', firstname='test', lastname='test', company_size='Under 5', agree=True)
    time.sleep(5)
    email_error = browser.find(xpath="//label[@for='content-download-form-email'][@class='error']")
    assert email_error and email_error.is_displayed(), 'No error displayed for non business email'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_success_download_form(browser):
    submit_content_download_form(browser, email='test@fyle.in', firstname='test', lastname='test', company_size='Under 5', agree=True)
    time.sleep(5)
    assert_content_download_thank_you_page(browser,'Automating T&E Management for SMBs in 2019','test@fyle.in','https://fyle-1.wistia.com/medias/0nakpa8v7g')
    browser.back()

