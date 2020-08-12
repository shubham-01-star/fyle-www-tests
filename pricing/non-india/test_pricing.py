import logging
import time
import pytest
from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + "/pricing")
    module_browser.set_local_storage('ipInfo', '{"ip":"157.50.160.253","country":"United States"}')
    module_browser.refresh()
    time.sleep(4)
    return module_browser

# check customer logo section (common section)
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_logo(browser):
    indian_logo = browser.find("//div[contains(@class, 'customer-logo-india')]")
    us_logo = browser.find("//div[contains(@class, 'customer-logo-non-india')]")
    assert us_logo.is_displayed() and not indian_logo.is_displayed(), 'Found an Indian image in US IP'

# check pricing: US prices should be shown
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_pricing_text(browser):
    standard_price = browser.find(xpath="//h2[contains(@class, 'standard-price')]")
    business_price = browser.find(xpath="//h2[contains(@class, 'business-price')]")
    assert standard_price.text == '$4.99' and business_price.text == '$8.99', 'Pricing is incorrect for non-India'
    standard_card_cta = browser.find("//div[contains(@class, 'card-footer')]//button[contains(@class, 'btn-outline-primary') and contains(text(), 'Get started')]")
    business_card_cta = browser.find("//div[contains(@class, 'card-footer')]//button[contains(@class, 'btn-primary') and contains(text(), 'Get a demo')]")
    assert standard_card_cta and business_card_cta, 'Pricing cards cta text is wrong'

# check annual/monthly toggle functionality: default should be annually
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_pricing_toggle(browser):
    standard_price = browser.find(xpath="//h2[contains(@class, 'standard-price')]")
    business_price = browser.find(xpath="//h2[contains(@class, 'business-price')]")
    assert business_price.text == '$8.99' and standard_price.text == '$4.99', 'Default annual pricing is incorrect for non-India'
    annual_price_active = browser.find(xpath="//label[contains(text(), 'Annually') and contains(@class, 'switch-active-text-color')]")
    browser.click_element(annual_price_active)
    monthly_price_active = browser.find(xpath="//label[contains(text(), 'Monthly') and contains(@class, 'switch-active-text-color')]")
    assert monthly_price_active and standard_price.text == '$6.99' and business_price.text == '$11.99', 'Toggle pricing button is not working'
