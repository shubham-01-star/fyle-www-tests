import time
import logging
import pytest
from simplebrowser import SimpleBrowser
from common.utils import resize_browser

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    time.sleep(0.5)
    module_browser.get(base_url + '/templates/expense-reports')
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_download_for_excel_form_modal(browser):
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

def submit_download_excel_form(browser, email=None, firstname=None, lastname=None, company_size=None, agree=None):
    browser.click(xpath="//a[@id='download-excel']")
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
    browser.click(xpath="//form[contains(@id, 'content-download-form')]//button[text()='Download']")

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_required_fields(browser):
    submit_download_excel_form(browser)
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
    submit_download_excel_form(browser, firstname='test1', lastname='test2')
    firstname_error = browser.find(xpath="//label[@for='content-download-form-first-name'][@class='error']")
    lastname_error = browser.find(xpath="//label[@for='content-download-form-last-name'][@class='error']")
    assert firstname_error and firstname_error.is_displayed(), "No error displayed for invalid firstname"
    assert lastname_error and lastname_error.is_displayed(), "No error displayed for invalid lastname"

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email(browser):
    submit_download_excel_form(browser, email='test')
    email_error = browser.find(xpath="//label[@for='content-download-form-email'][@class='error']")
    assert email_error and email_error.is_displayed(), 'No error displayed for invalid email'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_non_business_email(browser):
    submit_download_excel_form(browser, email='test@gmail.com', firstname='test', lastname='test', company_size='Under 5', agree=True)
    time.sleep(5)
    email_error = browser.find(xpath="//label[@for='content-download-form-email'][@class='error']")
    assert email_error and email_error.is_displayed(), 'No error displayed for non business email'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success_download_form(browser):
    submit_download_excel_form(browser, email='test@fyle.in', firstname='test', lastname='test', company_size='Under 5', agree=True)
    time.sleep(2)
    last_downloaded_filename = browser.get_downLoadeded_filename()
    time.sleep(4)
    browser.close_windows()
    assert last_downloaded_filename == 'https://cdn2.hubspot.net/hubfs/3906991/simple-expense-report-template.xlsx', "Downloaded file is not correct"

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_redirection_of_h2_cards(browser):
    time.sleep(2)
    card_link = 'https://ww2.fylehq.com/expense-report-software'
    card_blocks = [
        "//h2[contains(text(), 'See how expense reports should be done in 2020.')]//parent::a[contains(@class, 'report-template-style')]",
        "//h2[contains(text(), 'Find receipts buried in your inbox in seconds.')]//parent::a[contains(@class, 'report-template-style')]",
        "//h2[contains(text(), 'Log mileage & scan receipts on the same app.')]//parent::a[contains(@class, 'report-template-style')]"
    ]
    for i, card_block in enumerate(card_blocks):
        time.sleep(2)
        card = browser.find(xpath=card_block, scroll=True)
        card.click()
        assert browser.get_current_url() == card_link, f"{ i+1 } card link redirection is not successful"
        time.sleep(2)
        browser.back()
        browser.close_windows()

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_expense_report_and_mileage_log_template_urls(browser):
    time.sleep(2)
    template_links = [
        'https://templates.office.com/en-us/expense-report-tm04099206',
        'https://templates.office.com/en-us/Travel-expense-report-form-TM03463093',
        'https://templates.office.com/en-us/mileage-log-and-expense-report-tm16400627',
        'https://templates.office.com/en-us/Mileage-log-TM02808644'
    ]
    template_list = browser.find_many(
        xpath="//h3[not(contains(text(), 'Reimbursement Claim Sheet Templates'))]//parent::div//a[contains(@class, 'template-card')]")
    for i, template in enumerate(template_list):
        time.sleep(2)
        template.click()
        time.sleep(2)
        browser.switch_tab_next(1)
        time.sleep(5)
        assert browser.get_current_url() == template_links[i], "Expense report/ mileage log template url is not correct"
        browser.close_windows()
        time.sleep(2)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_reimbursement_template(browser):
    time.sleep(2)
    template_links = [
        'https://d2myx53yhj7u4b.cloudfront.net/sites/default/files/IC-ExpenseSheet.xlsx',
        'https://d2myx53yhj7u4b.cloudfront.net/sites/default/files/IC-MonthlyIncomeAndExpense.xlsx'
    ]
    template_list = browser.find_many(
        xpath="//h3[contains(text(), 'Reimbursement Claim Sheet Templates')]//parent::div//a[contains(@class, 'template-card')]")
   
    for i, template in enumerate(template_list):
        time.sleep(2)
        template.click()
        time.sleep(2)
        last_downloaded_filename = browser.get_downLoadeded_filename()
        time.sleep(5)
        assert last_downloaded_filename == template_links[i], "Reibursement template downloaded is not correct"
        browser.close_windows()
        