from time import sleep
import logging
from common.asserts import assert_thank_you_modal

logger = logging.getLogger(__name__)

def submit_svb_top_email_form(browser, email=None):
    browser.find(xpath="//form[contains(@id, 'svb-email-form-top')]")
    sleep(2)
    if email:
        browser.input(xpath="//form[contains(@id, 'svb-email-form-top')]//input[@name='email']", keys=email)
    browser.click(xpath="//form[contains(@id, 'svb-email-form-top')]//button[text()='Get Started']")

def submit_svb_contact_form(browser, name=None, phone=None, company_size=None):
    if name:
        browser.input(xpath="//form[contains(@id, 'svb-contact-form')]//input[@name='firstname']", keys=name)
    if phone:
        browser.input(xpath="//form[contains(@id, 'svb-contact-form')]//input[@name='phone']", keys=phone)
    if company_size:
        browser.click(xpath="//form[contains(@id, 'svb-contact-form')]//input[@id='number_of_employees']")
        browser.click(xpath=f"//form[contains(@id, 'svb-contact-form')]//li[@data-value='{company_size}']")
    browser.click(xpath="//form[contains(@id, 'svb-contact-form')]//button[text()='Redeem Your Offer']")

def assert_required_fields_top(browser):
    submit_svb_top_email_form(browser)
    email_error = browser.find(xpath="//label[@for='svb-email'][@id='svb-email-form-top-email-label'][@class='error']")
    sleep(1)
    assert email_error and email_error.is_displayed(), 'No error displayed for invalid email'

def assert_bad_email_top(browser):
    submit_svb_top_email_form(browser, email='test')
    email_error = browser.find(xpath="//label[@for='svb-email'][@id='svb-email-form-top-email-label'][@class='error']")
    sleep(1)
    assert email_error and email_error.is_displayed(), 'No error displayed for invalid email'

def assert_non_business_email_top(browser):
    submit_svb_top_email_form(browser, email='test@gmail.com')
    sleep(5)
    email_error = browser.find(xpath="//label[@for='svb-email'][@id='svb-email-form-top-email-label'][@class='error']")
    assert email_error and email_error.is_displayed(), 'No error displayed for non business email'

def assert_success_form_top(browser):
    submit_svb_top_email_form(browser, email='test@fyle.in')
    sleep(5)
    svb_contact_form = browser.find(xpath="//div[@id='svb-contact-modal']")
    assert svb_contact_form and svb_contact_form.is_displayed(), 'Svb contact form is not displayed'

def assert_svb_contact_form_required_fields(browser):
    submit_svb_top_email_form(browser, email='test@fyle.in')
    sleep(5)
    submit_svb_contact_form(browser)
    name_error = browser.find(xpath="//label[@for='svb-first-name'][@class='error']")
    phone_error = browser.find(xpath="//form[contains(@id, 'svb-contact-form')]//label[@for='svb-phone'][@class='error']")
    company_size_error = browser.find(xpath="//form[contains(@id, 'svb-contact-form')]//label[@for='number_of_employees'][@class='error']")
    assert name_error and name_error.is_displayed(), "No error displayed for missing name"
    assert phone_error and phone_error.is_displayed(), "No error displayed for missing phone"
    assert company_size_error and company_size_error.is_displayed(), "No error displayed for missing company size"

def assert_svb_contact_form_invalid_name(browser):
    submit_svb_top_email_form(browser, email='test@fyle.in')
    sleep(5)
    submit_svb_contact_form(browser, name="test1")
    name_error = browser.find(xpath="//label[@for='svb-first-name'][@class='error']")
    assert name_error and name_error.is_displayed(), "No error displayed for invalid name"

def assert_svb_contact_form_invalid_phone(browser):
    submit_svb_top_email_form(browser, email='test@fyle.in')
    sleep(5)
    submit_svb_contact_form(browser, phone="123abc123")
    phone_error = browser.find(xpath="//form[contains(@id, 'svb-contact-form')]//label[@for='svb-phone'][@class='error']")
    assert phone_error and phone_error.is_displayed(), "No error displayed for invalid phone"

def assert_svb_contact_form_invalid_phone_length_min(browser):
    submit_svb_top_email_form(browser, email='test@fyle.in')
    sleep(5)
    submit_svb_contact_form(browser, phone="123")
    phone_error = browser.find(xpath="//form[contains(@id, 'svb-contact-form')]//label[@for='svb-phone'][@class='error']")
    assert phone_error and phone_error.is_displayed(), "No error displayed for invalid phone minlength"

def assert_svb_contact_form_invalid_phone_length_max(browser):
    submit_svb_top_email_form(browser, email='test@fyle.in')
    sleep(5)
    submit_svb_contact_form(browser, phone="123456789123456789")
    phone_error = browser.find(xpath="//form[contains(@id, 'svb-contact-form')]//label[@for='svb-phone'][@class='error']")
    assert phone_error and phone_error.is_displayed(), "No error displayed for invalid phone maxlength"

def assert_svb_contact_form_success(browser):
    sleep(1)
    submit_svb_top_email_form(browser, email='test@fyle.in')
    submit_svb_contact_form(browser, name='test', phone='123456789', company_size='Under 5')
    ty_message = 'Sit back and relax. Our Customer Success team will soon reach out to you and set up a call.'
    assert_thank_you_modal(browser, ty_message)
 