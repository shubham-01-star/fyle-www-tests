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

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_expense_report_and_mileage_log_template_urls(browser):
    template_links = [
        'https://templates.office.com/en-us/expense-report-tm04099206',
        'https://templates.office.com/en-us/Travel-expense-report-form-TM03463093',
        'https://templates.office.com/en-us/mileage-log-and-expense-report-tm16400627',
        'https://templates.office.com/en-us/Mileage-log-TM02808644'
    ]
    template_list = browser.find_many(
        xpath="//h3[not(contains(text(), 'Reimbursement Claim Sheet Templates'))]/parent::div//a[contains(@class, 'template-card')]")
    for i, template in enumerate(template_list):
        time.sleep(2)
        template.click()
        browser.switch_tab_next(1)
        time.sleep(5)
        assert browser.get_current_url() == template_links[i], "Expense report/ mileage log template url is not correct"
        browser.close_windows()

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_reimbursement_template(browser):
    template_links = [
        'http://d2myx53yhj7u4b.cloudfront.net/sites/default/files/IC-ExpenseSheet.xlsx',
        'http://d2myx53yhj7u4b.cloudfront.net/sites/default/files/IC-MonthlyIncomeAndExpense.xlsx'
    ]
    template_list = browser.find_many(
        xpath="//h3[contains(text(), 'Reimbursement Claim Sheet Templates')]/parent::div//a[contains(@class, 'template-card')]")
    for i, template in enumerate(template_list):
        time.sleep(2)
        template_href = template.get_attribute('href')
        time.sleep(5)
        assert template_href == template_links[i], "Reibursement download template link is not correct"
        
