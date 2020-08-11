import logging
import time
import pytest
from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + "/pricing")
    module_browser.set_local_storage('ipInfo', '{"ip":"157.50.160.253","country":"India"}')
    module_browser.refresh()
    time.sleep(5)
    return module_browser

# check customer logo section (common section)
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_logo(browser):
    indian_logo = browser.find("//div[contains(@class, 'customer-logo-india')]")
    us_logo = browser.find("//div[contains(@class, 'customer-logo-non-india')]")
    assert indian_logo.is_displayed() and not us_logo.is_displayed(), 'Found an Indian image in US IP'

# check pricing: Indian prices should be shown
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_pricing_text(browser):
    standard_price = browser.find(xpath="//h2[contains(@class, 'standard-price')]")
    business_price = browser.find(xpath="//h2[contains(@class, 'business-price')]")
    assert standard_price.text == 'Custom pricing' and business_price.text == 'Custom pricing', 'Pricing is incorrect for India'
    standard_card_cta = browser.find("//div[contains(@class, 'card-footer')]//button[contains(@class, 'btn-outline-primary') and contains(text(), 'Contact us')]")
    business_card_cta = browser.find("//div[contains(@class, 'card-footer')]//button[contains(@class, 'btn-primary') and contains(text(), 'Contact us')]")
    assert standard_card_cta and business_card_cta, 'Pricing cards cta text is wrong'
