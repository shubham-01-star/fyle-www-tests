import time
import logging
from common.asserts import assert_content_download_thank_you_page

logger = logging.getLogger(__name__)

def submit_content_download_form(browser, email=None, firstname=None, lastname=None, company_size=None, agree=None):
    if '/templates/expense-reports' in browser.get_current_url():
        browser.click(xpath="//a[@id='download-excel']")
    else:
        browser.find(xpath="//form[contains(@id, 'content-download-form')]", scroll=True)
    time.sleep(2)
    if firstname:
        browser.input(xpath="//form[contains(@id, 'content-download-form')]//input[@name='firstname']", keys=firstname)
    if lastname:
        browser.input(xpath="//form[contains(@id, 'content-download-form')]//input[@name='lastname']", keys=lastname)
    if email:
        browser.input(xpath="//form[contains(@id, 'content-download-form')]//input[@name='email']", keys=email)
    if company_size:
        browser.click(xpath="//form[contains(@id, 'content-download-form')]//input[@id='number_of_employees']")
        browser.click(xpath=f"//form[contains(@id, 'content-download-form')]//li[@data-value='{company_size}']")
    if agree:
        browser.click(xpath="//form[contains(@id, 'content-download-form')]//div[contains(@class, 'custom-checkbox')]")
    if '/templates/expense-reports' in browser.get_current_url():
        browser.click(xpath="//form[contains(@id, 'content-download-form')]//button[text()='Download']")
    else:
        browser.click(xpath="//form[contains(@id, 'content-download-form')]//button[contains(@id, 'form-button')]")

def assert_content_download_inline_form(browser):
    time.sleep(1)
    download_form = browser.find(xpath="//form[contains(@id, 'content-download-form')]")
    assert download_form.is_displayed(), "inline form is not present"
    h3_head = browser.find(xpath="//h3[contains(@id, 'report-heading')]")
    assert h3_head and h3_head.is_displayed(), "Form h3 heading is not displayed"
    sub_text = browser.find(xpath="//p[contains(@id, 'report-subtext')]")
    assert sub_text and sub_text.is_displayed(), "Form sub-heading is not displayed"

def assert_download_for_excel_form_modal(browser):
    download_modal_cta = browser.find(xpath="//a[contains(@id, 'download-excel')]")
    time.sleep(2)
    download_modal_cta.click()
    time.sleep(2)
    report_modal = browser.find(xpath="//div[contains(@id, 'expense-report-modal')]")
    assert report_modal.is_displayed(), "modal is not opened"
    time.sleep(2)
    h3_head = browser.find(xpath="//h3[contains(@id, 'report-heading')]")
    assert h3_head and h3_head.is_displayed(), "Modal h3 heading is not displayed"
    sub_text = browser.find(xpath="//p[contains(@id, 'report-subtext')]")
    assert sub_text and sub_text.is_displayed(), "Modal sub-heading is not displayed"
    close_button = browser.find(xpath="//div[contains(@id, 'expense-report-modal')]//button[contains(@class, 'close')]")
    close_button.click()
    time.sleep(2)
    assert not report_modal.is_displayed(), "modal is not closed"

def assert_required_fields(browser):
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

def assert_invalid_names(browser):
    submit_content_download_form(browser, firstname='test1', lastname='test2')
    firstname_error = browser.find(xpath="//label[@for='content-download-form-first-name'][@class='error']")
    lastname_error = browser.find(xpath="//label[@for='content-download-form-last-name'][@class='error']")
    assert firstname_error and firstname_error.is_displayed(), "No error displayed for invalid firstname"
    assert lastname_error and lastname_error.is_displayed(), "No error displayed for invalid lastname"

def assert_bad_email(browser):
    submit_content_download_form(browser, email='test')
    email_error = browser.find(xpath="//label[@for='content-download-form-email'][@class='error']")
    assert email_error and email_error.is_displayed(), 'No error displayed for invalid email'

def assert_non_business_email(browser):
    time.sleep(1)
    submit_content_download_form(browser, email='test@gmail.com', firstname='test', lastname='test', company_size='Under 5', agree=True)
    time.sleep(5)
    email_error = browser.find(xpath="//label[@for='content-download-form-email'][@class='error']")
    assert email_error and email_error.is_displayed(), 'No error displayed for non business email'

def assert_success_download_form(browser):
    submit_content_download_form(browser, email='test@fyle.in', firstname='test', lastname='test', company_size='Under 5', agree=True)
    time.sleep(5)
    if '/templates/expense-reports' in browser.get_current_url():
        time.sleep(2)
        last_downloaded_filename = browser.get_downLoadeded_filename()
        time.sleep(4)
        browser.close_windows()
        assert last_downloaded_filename == 'https://cdn2.hubspot.net/hubfs/3906991/simple-expense-report-template.xlsx', "Downloaded file is not correct"
    else:
        assert_content_download_thank_you_page(browser,'Realtime visibility into T&E for Zivame','test@fyle.in','https://cdn2.hubspot.net/hubfs/3906991/Case%20Study%20/Fyle-Zivame-Case-Study.pdf')
        browser.back()

