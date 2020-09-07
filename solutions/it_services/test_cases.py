import logging
from time import sleep
import pytest

from common.utils import resize_browser
from common.asserts import assert_cta_click_and_modal_show, assert_customer_logo
from common.asserts import assert_overflowing, assert_click_scroll_into_view
from common.test_getdemo import assert_bad_email, assert_missing_firstname, assert_success

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + "/solutions/industry/information-technology")
    sleep(4)
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_page_overflow(browser):
    assert_overflowing(browser)

# Check demo form (common section)
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email(browser):
    assert_bad_email(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_missing_firstname(browser):
    assert_missing_firstname(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success(browser):
    assert_success(browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_hero_section_cta(browser):
    cta_section_xpath = "//section[contains(@class, 'new-hero')]"
    cta_xpath = f"{cta_section_xpath}//div[not(contains(@class, 'demo-button-until-banner'))]/a"
    assert_cta_click_and_modal_show(browser, cta_section_xpath, cta_xpath)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_hero_section_clickable_bullets(browser):
    clickable_elements_xpath = "//section[contains(@class, 'new-hero')]//div[contains(@class, 'scroll-to-bullets')]//div"
    assert_click_scroll_into_view(browser, clickable_elements_xpath)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_customer_logo_section(browser):
    assert_customer_logo(browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_sticky_slider_feature_section(browser):
    clickable_elements_xpath = "//section[contains(@class, 'sticky-slider-feature-section')]//div[contains(@class, 'sticky-sidebar')]//li"
    assert_click_scroll_into_view(browser, clickable_elements_xpath)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_feature_section_spacing(browser):
    section_xpath = "//section[contains(@class, 'sticky-slider-feature-section')]"
    assert_spacing_between_text_image(browser, section_xpath)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_bottom_section_cta(browser):
    cta_section_xpath = '//section[contains(@class, "bottom-stat-with-cta")]'
    cta_xpath = f'{cta_section_xpath}//a'
    assert_cta_click_and_modal_show(browser, cta_section_xpath, cta_xpath)
