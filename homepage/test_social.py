import os
import time
from simplebrowser import SimpleBrowser
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture
def browser(module_browser):
    module_browser.get('https://www.fylehq.com')
    return module_browser

def test_twitter(browser):
    e = browser.find(xpath="//a[@href='https://twitter.com/FyleHQ']", scroll=True)
    assert e and e.is_displayed(), 'twitter link not there'
