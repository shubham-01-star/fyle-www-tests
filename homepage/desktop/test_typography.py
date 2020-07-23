import time
from simplebrowser import SimpleBrowser
import logging
import pytest
from common.asserts import assert_typography

logger = logging.getLogger(__name__)

@pytest.fixture
def browser(module_browser, base_url):
    assert module_browser.is_desktop(), 'this test can only be run on desktops'
    module_browser.get(base_url)
    return module_browser

def test_typography(browser):
    assert_typography(browser=browser)
