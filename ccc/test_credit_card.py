import os
import time
from simplebrowser import SimpleBrowser
import logging
import pytest
from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    module_browser.get(base_url + '/corporate-credit-cards')
    time.sleep(3)
    return module_browser

def play_ccc_hero_video(browser):
    time.sleep(1)
    browser.click(xpath="//div[contains(@class, 'play-button')]")
    time.sleep(5)

def test_ccc_video(browser):
    play_ccc_hero_video(browser)
    e = browser.find(xpath="//div[contains(@class, 'feature-hero-video')]//iframe")
    assert e and e.is_displayed(), 'Video not played'

def test_video_thumbnail(browser):
    browser.find("//div[contains(@class, 'feature-hero-video')]//img", scroll=True)
    img = browser.driver.find_elements_by_xpath("//div[contains(@class, 'feature-hero-video')]//div[contains(@class, 'youtube')]//img")
    script = "return(typeof arguments[0].naturalWidth!=\"undefined\" && arguments[0].naturalWidth>0)"
    time.sleep(1)
    e = browser.driver.execute_script(script, img[0])
    assert e, 'Image not loaded'

def test_customer_logo(browser):
    ip_info = browser.get_from_storage('ipInfo')
    country = ip_info['country']
    if country == 'India':
        logo_div = browser.find("//div[contains(@class, 'customer-logo-non-india') and contains(@class, 'd-none')]")
        logger.info(logo_div)
        assert logo_div, 'Found an US image in Indian IP'
    else:
        logo_div = browser.find("//div[contains(@class, 'customer-logo-india') and contains(@class, 'd-none')]")
        assert logo_div, 'Found an Indian image in other IP'

def test_badges(browser):
    total_badges = browser.find_many("//div[contains(@class, 'fyle-badge')]")
    hidden_badges = browser.find_many("//div[contains(@class, 'fyle-badge') and contains(@style, 'display: none;')]")
    assert (len(total_badges) - len(hidden_badges)) == 1, 'Badges aren\'t properly displayed.'

def test_sneak_peek(browser):
    sneak_peak_tabs = browser.find_many("//div[contains(@class, 'tab-section')]//a[contains(@class, 'nav-link')]")
    tabs_checked = 0
    for tab in sneak_peak_tabs:
        browser.hover(tab)
        active_tab = browser.find_many("//div[contains(@class, 'tab-section')]//a[contains(@class, 'nav-link') and contains(@class, 'active')]")
        if (len(active_tab) == 1) and (tab == active_tab[0]):
            tabs_checked += 1
    assert tabs_checked == len(sneak_peak_tabs), 'Error in sneak peek tabs'
