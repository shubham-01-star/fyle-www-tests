from time import sleep
import logging
import pytest
from common.utils import resize_browser
from common.asserts import assert_overflowing, assert_typography, assert_collapse_sneak_peek_desktop, assert_collapse_sneak_peek_desktop_spacing, assert_new_gradient_hero_section_typography, assert_collapse_sneak_peek_mobile_spacing, assert_collapse_sneak_peek_mobile
logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/solutions/industry/construction')
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
    assert_collapse_sneak_peek_desktop_spacing(browser)

@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_collapse_sneak_peek_section_spacing_mobile(browser):
    assert_collapse_sneak_peek_mobile_spacing(browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_collapse_sneak_peek_section_desktop(browser):
    assert_collapse_sneak_peek_desktop(browser)

@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_collapse_sneak_peek_section_mobile(browser):
    assert_collapse_sneak_peek_mobile(browser)
