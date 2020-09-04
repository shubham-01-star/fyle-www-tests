from time import sleep
import logging
import pytest
from common.utils import resize_browser
from common.asserts import assert_overflowing, assert_typography, assert_collapse_sneak_peek_desktop, assert_collapse_sneak_peek_desktop_spacing, assert_new_gradient_hero_section_typography
logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/automated-expense-reporting')
    sleep(4)
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_overflowing(browser):
    assert_overflowing(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_hero_typography(browser):
    assert_new_gradient_hero_section_typography(browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_collapse_sneak_peek_section_spacing_desktop(browser):
    card_header = browser.find_many(xpath="//section[contains(@class,'partner-collapsible-section')]//div[contains(@class, 'collapsible-card-header')]")
    card_content_xpath = "//section[contains(@class,'partner-collapsible-section')]//div[contains(@class, 'collapsible-card-body') and contains(@class, 'show')]//div[contains(@class, 'card-content')]"
    assert_collapse_sneak_peek_desktop_spacing(browser, card_header, card_content_xpath)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_collapse_sneak_peek_section_desktop(browser):
    card_header = browser.find_many(xpath="//section[contains(@class,'partner-collapsible-section')]//div[contains(@class, 'collapsible-card-header')]")
    card_body_xpath = "//section[contains(@class,'partner-collapsible-section')]//div[contains(@class, 'collapsible-card-body') and contains(@class, 'show')]"
    assert_collapse_sneak_peek_desktop(browser, card_header, card_body_xpath)
    