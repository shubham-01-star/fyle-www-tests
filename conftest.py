from simplebrowser import SimpleBrowser
import logging
import pytest
import os
import time

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def base_url():
   return 'https://ww2.fylehq.com'

# testdata_all = [
#    ('chrome', '1920', '1080'),
#    ('chrome', '1536', '864'),
#    ('chrome', '414', '896'),
# ]

# testdata_fast = [
#    ('chrome', '1920', '1080'),
#    ('chrome', '414', '896'),
# ]

@pytest.fixture(scope='module')
def module_browser(base_url):
   browser = os.getenv('BROWSER', 'chrome')
   width = int(os.getenv('WIDTH', '1920'))
   height = int(os.getenv('HEIGHT', '1080'))
   logger.debug('creating browser %s, width %s, height %s', browser, width, height)
   sb = SimpleBrowser(browser=browser, width=width, height=height)
   sb.get(base_url)
   sb.click(xpath="//span[contains(@class, 'banner-close')]")
   return sb
