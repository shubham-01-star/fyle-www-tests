from time import sleep
import logging
import pytest
from common.utils import resize_browser
from common.asserts import assert_spacing_between, assert_spacing_bottom, assert_spacing_top, assert_spacing_right, assert_spacing_left, assert_overflowing, assert_customer_testimonial, assert_customer_logo, assert_typography, assert_cards_redirection

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/partners/small-business-bookkeeping')
    sleep(4)
    return module_browser

# @pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
# def test_overflowing(browser):
#     assert_overflowing(browser=browser)

# @pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
# def test_typography(browser):
#     assert_typography(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_collapse_sneak_peek_section(browser):
    collapse_card_list = browser.find_many("//section[contains(@class,'partner-collapsible-section')]//div[contains(@class, 'collapsible-card')]")
    # for card in collapse_card_list:
    #     browser.scroll_up_or_down(300)
    #     browser.click(card)
    