from simplebrowser import SimpleBrowser
import logging
import pytest
import os
import time

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def module_browser():
    browser = os.getenv('BROWSER', 'chrome')
    logger.debug('creating browser %s', browser)
    module_browser = SimpleBrowser(browser=browser)
    module_browser.get('https://www.fylehq.com')
    module_browser.input(xpath="//span[@class='banner-close']", click=True)
    return module_browser
