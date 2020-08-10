import time
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture
def browser(module_browser, base_url):
    module_browser.get(base_url + '/expensify-alternative')
    return module_browser

def test_redirection(browser):
    time.sleep(3)
    e = browser.find(xpath="//h1")
    assert e.text == 'The best Expensify alternative in 2020', 'Not redirecting to the right page'
