import logging

import pytest

from common.utils import create_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def base_url():
    return 'https://ww2.fylehq.com'

@pytest.fixture(scope='module')
def module_browser(base_url):
    browser = create_browser()
    browser.get(base_url)
    browser.click(xpath="//span[contains(@class, 'banner-close')]")
    yield browser
    del browser
