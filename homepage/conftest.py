from simplebrowser import SimpleBrowser
import logging
import pytest
import os
import time

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def module_browser():
    browser = os.getenv('BROWSER', 'chrome')
    device = None
 #   device = os.getenv('DEVICE', None)
    logger.debug('creating browser %s, device %s', browser, device)
    module_browser = SimpleBrowser(browser=browser, device=device)
    module_browser.get('https://www.fylehq.com')
    module_browser.input(xpath="//span[@class='banner-close']", click=True)
    return module_browser
