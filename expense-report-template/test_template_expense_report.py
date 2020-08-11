from time import sleep
import logging
import pytest
from common.utils import resize_browser
from common.asserts import assert_typography, assert_overflowing
from common.content_download_form import assert_download_for_excel_form_modal, assert_required_fields, assert_invalid_names, assert_bad_email, assert_non_business_email, assert_success_download_form

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/templates/expense-reports')
    sleep(2)
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_page_overflow(browser):
    assert_overflowing(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_typography(browser):
    assert_typography(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_content_download_inline_form(browser):
    assert_download_for_excel_form_modal(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_required_fields(browser):
    assert_required_fields(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_invalid_names(browser):
    assert_invalid_names(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email(browser):
    assert_bad_email(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_non_business_email(browser):
    assert_non_business_email(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success_download_form(browser):
    assert_success_download_form(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_redirection_of_h2_cards(browser):
    card_link = 'https://ww2.fylehq.com/expense-report-software'
    card_blocks = [
        "//h2[contains(text(), 'See how expense reports should be done in 2020.')]//parent::a[contains(@class, 'report-template-style')]",
        "//h2[contains(text(), 'Find receipts buried in your inbox in seconds.')]//parent::a[contains(@class, 'report-template-style')]",
        "//h2[contains(text(), 'Log mileage & scan receipts on the same app.')]//parent::a[contains(@class, 'report-template-style')]"
    ]
    for i, card_block in enumerate(card_blocks):
        card = browser.find(xpath=card_block, scroll=True)
        browser.click_element(card)
        assert browser.get_current_url() == card_link, f"{ i+1 } card link redirection is not successful"
        browser.back()
        browser.close_windows()

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_expense_report_and_mileage_log_template_urls(browser):
    template_links = [
        'https://templates.office.com/en-us/expense-report-tm04099206',
        'https://templates.office.com/en-us/Travel-expense-report-form-TM03463093',
        'https://templates.office.com/en-us/mileage-log-and-expense-report-tm16400627',
        'https://templates.office.com/en-us/Mileage-log-TM02808644'
    ]
    template_list = browser.find_many(
        xpath="//h3[not(contains(text(), 'Reimbursement Claim Sheet Templates'))]//parent::div//a[contains(@class, 'template-card')]")
    for i, template in enumerate(template_list):
        browser.click_element(template)
        browser.switch_tab_next(1)
        assert browser.get_current_url() == template_links[i], "Expense report/ mileage log template url is not correct"
        browser.close_windows()

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_reimbursement_template(browser):
    template_links = [
        'https://d2myx53yhj7u4b.cloudfront.net/sites/default/files/IC-ExpenseSheet.xlsx',
        'https://d2myx53yhj7u4b.cloudfront.net/sites/default/files/IC-MonthlyIncomeAndExpense.xlsx'
    ]
    template_list = browser.find_many(
        xpath="//h3[contains(text(), 'Reimbursement Claim Sheet Templates')]//parent::div//a[contains(@class, 'template-card')]")
    for i, template in enumerate(template_list):
        browser.click_element(template)
        last_downloaded_filename = browser.get_downLoadeded_filename()
        assert last_downloaded_filename == template_links[i], "Reibursement template downloaded is not correct"
        browser.close_windows()
        