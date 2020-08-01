import logging
import time

import pytest

from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + "/pricing")
    return module_browser

@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_collapsible_details(browser):
    browser.click(xpath="//a[@id='show-hide-standard']")
    details_display = browser.get_computed_style(xpath="//a[@id='standard-collapse']", key="display")
    assert details_display == 'block', 'Show details is not opening the collapsible'

@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_sticky_table_header(browser):
    browser.scroll_into_view(xpath="//div[contains(@class, 'table-data') and contains(text(), 'Real-time Policy Violations')]")
    header_position = browser.get_computed_style(xpath="//div[contains(@class, 'table-head')]", key="position")
    assert header_position == 'sticky', 'Compare all plans table header is not sticky'