import logging

logger = logging.getLogger(__name__)

def submit_content_download_form(browser, email=None, firstname=None, lastname=None, company_size=None, agree=None):
    if '/templates/expense-reports' in browser.get_current_url():
        browser.click(xpath="//a[@id='download-excel']")
    else:
        browser.find(xpath="//form[contains(@id, 'content-download-form')]", scroll=True)
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
    download_form = browser.find(xpath="//form[contains(@id, 'content-download-form')]")
    assert download_form.is_displayed(), "inline form is not present"
    h3_head = browser.find(xpath="//h3[contains(@id, 'report-heading')]")
    assert h3_head and h3_head.is_displayed(), "Form h3 heading is not displayed"
    sub_text = browser.find(xpath="//p[contains(@id, 'report-subtext')]")
    assert sub_text and sub_text.is_displayed(), "Form sub-heading is not displayed"

def assert_download_for_excel_form_modal(browser):
    download_modal_cta = browser.find(xpath="//a[contains(@id, 'download-excel')]")
    browser.click_element(download_modal_cta)
    report_modal = browser.find(xpath="//div[contains(@id, 'expense-report-modal')]")
    assert report_modal.is_displayed(), "modal is not opened"
    h3_head = browser.find(xpath="//h3[contains(@id, 'report-heading')]")
    assert h3_head and h3_head.is_displayed(), "Modal h3 heading is not displayed"
    sub_text = browser.find(xpath="//p[contains(@id, 'report-subtext')]")
    assert sub_text and sub_text.is_displayed(), "Modal sub-heading is not displayed"
    close_button = browser.find(xpath="//div[contains(@id, 'expense-report-modal')]//button[contains(@class, 'close')]")
    browser.click_element(close_button)
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
    submit_content_download_form(browser, email='test@gmail.com', firstname='test', lastname='test', company_size='Under 5', agree=True)
    email_error = browser.find(xpath="//label[@for='content-download-form-email'][@class='error']")
    assert email_error and email_error.is_displayed(), 'No error displayed for non business email'

def assert_success_download_form(browser, title=None, email=None, content_url=None):
    submit_content_download_form(browser, email='test@fyle.in', firstname='test', lastname='test', company_size='Under 5', agree=True)
    if '/templates/expense-reports' in browser.get_current_url():
        last_downloaded_filename = browser.get_downLoadeded_filename()
        browser.close_windows()
        assert last_downloaded_filename == 'https://cdn2.hubspot.net/hubfs/3906991/simple-expense-report-template.xlsx', "Downloaded file is not correct"
    else:
        assert_content_download_thank_you_page(browser, title, email, content_url)
        browser.back()

def assert_content_download_thank_you_page(browser, title, email, content_url):
    url = browser.get_current_url()
    assert '/thank-you' in url, "Thank you page is not displayed"
    page_title = browser.find(xpath="//section[contains(@class, 'resource-thank-you')]//span[contains(@class, 'thank-you-page-title')]").text
    assert title == page_title, "Content title is not correct"
    user_email = browser.find(xpath="//section[contains(@class, 'resource-thank-you')]//span[contains(@class, 'thank-you-page-email')]").text
    assert email == user_email, "User email is not correct"
    url_link = browser.find(xpath="//section[contains(@class, 'resource-thank-you')]//a[contains(@id, 'download-link')]")
    browser.click_element(url_link)
    browser.switch_tab_next(1)
    assert browser.get_current_url() == content_url, "Content download link is correct"
    browser.close_windows()
    random_cards = browser.find_many(xpath="//section[contains(@class, 'random-card-section')]//a//h4")
    for i, resource in enumerate(random_cards):
        assert resource.text != title, "Random cards are not properly generated"
