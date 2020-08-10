import time
import logging
import pytest

from common.asserts import assert_overflowing
from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    time.sleep(0.5)
    module_browser.get(base_url + "/expense-management")
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_feature_scroll(browser):
    browser.click(xpath="//section[@class='feature-hero']//a[text()='Expense Reporting']")
    time.sleep(2)
    e = browser.find(xpath="//section[@id='expense-reporting']")
    assert abs(e.location['y'] - browser.current_scroll_position()) <= 30, 'Not scrolling to the Expense Reporting feature'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_collpasing_section(browser):
    for i in range(1, 11):
        section = browser.click(xpath=f"//a[@id='feature-{i}']")
        class_list = section.get_attribute('class')
        assert class_list.count('collapse-closed collapsed'), 'Collapsing of sections should work'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_overflowing(browser):
    assert_overflowing(browser=browser)
