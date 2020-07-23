from simplebrowser import SimpleBrowser
import logging
import os
import time

logger = logging.getLogger(__name__)

resolutions = {
    'desktop_1': {'width': 1536, 'height': 864 },
    'mobile_1': {'width': 414, 'height': 896 }
}

def create_browser():
    name = os.getenv('BROWSER', 'chrome')
    width = 1920
    height = 1080
    logger.debug('creating browser %s, width %s, height %s', name, width, height)
    browser = SimpleBrowser(browser=name, width=width, height=height)
    return browser

def resize_browser(browser, resolution):
    width = resolutions[resolution]['width']
    height = resolutions[resolution]['height']
    browser.set_window_size(width=width, height=height)
    return browser
