import time
import logging
import pytest
from common.utils import resize_browser
from common.asserts import assert_hero_image

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/alternative/expensify')
    return module_browser

@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_hero_image(browser):
    assert_hero_image(browser=browser)
