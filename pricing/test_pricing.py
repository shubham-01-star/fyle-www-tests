import os
import time
from simplebrowser import SimpleBrowser
import logging
import pytest

logger = logging.getLogger(__name__)

# base url; read about @pytest.fixture

@pytest.fixture
def browser(module_browser, base_url):
    module_browser.get(base_url + "/pricing")
    return module_browser

def test_bcp_redirection(browser):
    browser.click(xpath="//a[contains(text(), 'Click here')]")
    # e = browser.find(xpath="//h3[contains(text(), 'Business continuity at Fyle:')]")
    e = browser.find(xpath="//h1")
    e.text == 'Business continuity at Fyle:'
    assert e.text, 'Redirection fails'

# def test_bcp_redirection(browser):
#     browser.click(xpath="//a[contains(text(), 'Click here')]")
#     e = browser.find(xpath="//h3[contains(text(), 'Business continuity at Fyle:')]")
#     assert e and e.is_displayed(), 'Redirected successfully to BCP page'