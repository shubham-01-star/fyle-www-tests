import os
import time
from simplebrowser import SimpleBrowser
import logging
import pytest
from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    time.sleep(0.5)
    module_browser.get(base_url + "/expense-management")
    time.sleep(3)
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_feature_scroll(browser):
    result = False
    browser.click(xpath="//section[@class='feature-hero']//a[text()='Expense Reporting']")
    time.sleep(2)
    e = browser.find(xpath="//section[@id='expense-reporting']")
    if abs(e.location['y'] - browser.current_scroll_position()) <= 30:
        result = True
    assert result, 'Not scrolling to the section'