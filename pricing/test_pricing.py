import os
import time
from simplebrowser import SimpleBrowser
import logging
import pytest

logger = logging.getLogger(__name__)

# base url; read about @pytest.fixture

@pytest.fixture
def browser(module_browser, base_url):
    module_browser.get(base_url + "/pricing")
    return module_browser

# check pricing page is redirecting to bcp page 
def test_bcp_redirection(browser):
    browser.click(xpath="//a[contains(text(), 'Click here')]")
    e = browser.find(xpath="//h1")
    e.text == 'Business continuity at Fyle:'
    assert e.text, 'Redirection fails'

# check toggle of compare plans table
def test_compareplan_table(browser):
    e_hidden = browser.find(xpath="//div[contains(@class, 'feature-table') and contains(@class, 'd-none')]")
    browser.click(xpath="//button[contains(text(), 'Compare all plans')]")
    e_visible = browser.find(xpath="//div[contains(@class, 'feature-table') and not(contains(@class, 'd-none'))]")
    assert e_hidden and e_visible, 'Not opening compare all plans table'

# check download form is opening on clicking the cta present inside the table
def test_download_cta(browser):
    browser.click(xpath="//button[contains(text(), 'Compare all plans')]")
    browser.click(xpath="//button[contains(@class, 'download-feature')]")
    e = browser.find(xpath="//div[@id='all-feature-modal']")
    assert e, 'All feature modal is missing'

# check pricing for US and India
def test_pricing(browser):
    ip_info = browser.get_from_storage('ipInfo')
    country = ip_info['country']
    standard_price = browser.find(xpath="//h2[contains(@class, 'standard-price')]")
    business_price = browser.find(xpath="//h1[contains(@class, 'business-price')]")

    if country == 'India':
        assert standard_price.text == 'Custom Pricing' and business_price.text == 'Custom Pricing', 'Pricing text is incorrect'
    else:
        assert standard_price.text == '$4.99' and business_price.text == '$8.99', 'Pricing is incorrect for non-India ip'

# check annual/monthly toggle functionality
def test_pricing_toggle(browser):
    ip_info = browser.get_from_storage('ipInfo')
    country = ip_info['country']
    standard_price = browser.find(xpath="//h2[contains(@class, 'standard-price')]")
    business_price = browser.find(xpath="//h1[contains(@class, 'business-price')]")

    if country != 'India':
        annual_price_active = browser.find(xpath="//label[contains(text(), 'Annually') and contains(@class, 'switch-active-text-color')]")
        annual_price_active.click()
        monthly_price_active = browser.find(xpath="//label[contains(text(), 'Monthly') and contains(@class, 'switch-active-text-color')]")
        assert monthly_price_active and standard_price.text == '$6.99' and business_price.text == '$11.99'


# check all 3 pricing cards have cta which open demo form
# def test_cards_cta(browser):
#     card_ctas =  browser.find_many("//div[contains(@class, 'card-footer')]")
#     outside_card = browser.find("//body")
#     for cta in card_ctas:
#         cta.click()
#         outside_card.click()