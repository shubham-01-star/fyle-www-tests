from time import sleep
import logging

logger = logging.getLogger(__name__)

def submit_chrome_uninstall_form(browser, email=None, feedback=None ):
    browser.find(xpath="//form[contains(@id, 'send-feedback')]", scroll=True)
    if email:
        browser.input(xpath="//form[contains(@id, 'send-feedback')]//input[@name='email']", keys=email)
    if feedback:
        browser.input(xpath="//form[contains(@id, 'send-feedback')]//textarea[@name='extension_feedback']", keys=feedback)
    browser.click(xpath="//form[contains(@id, 'send-feedback')]//button[text()='Send Feedback']")

def assert_required_fields(browser):
    submit_chrome_uninstall_form(browser)
    email_error = browser.find(xpath="//label[@for='feedback-email'][@class='error']")
    feedback_error = browser.find(xpath="//label[@for='uninstall-description'][@class='error']")
    sleep(1)
    assert email_error and email_error.is_displayed(), 'No error displayed for missing email'
    assert feedback_error and feedback_error.is_displayed(), 'No error displayed for missing feedback'

def assert_invalid_email(browser):
    submit_chrome_uninstall_form(browser, email="test")
    email_error = browser.find(xpath="//label[@for='feedback-email'][@class='error']")
    sleep(1)
    assert email_error and email_error.is_displayed(), 'No error displayed for invalid email'

# def assert_non_business_email(browser):
#     submit_chrome_uninstall_form(browser, email="test@gmail.com")
#     email_error = browser.find(xpath="//label[@for='feedback-email'][@class='error']")
#     sleep(5)
#     assert email_error and email_error.is_displayed(), 'No error displayed for non business email'

def assert_success_chrome_uninstall_form(browser):
    submit_chrome_uninstall_form(browser, email="test@fyle.in", feedback='test feedback')
    sleep(5)
    ty_message = browser.find(xpath="//form[contains(@id, 'send-feedback')]//p[contains(@class, 'feedback-submit')]")
    assert ty_message and ty_message.is_displayed(), 'No error displayed for invalid email'