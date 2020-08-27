import time
import logging
import pytest

from common.asserts import assert_customer_logo
from common.asserts import assert_badges
from common.asserts import assert_customer_testimonial
from common.asserts import assert_typography
from common.asserts import assert_overflowing
from common.utils import resize_browser
from common.test_getdemo import assert_bad_email, assert_missing_firstname, assert_success

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/corporate-credit-cards')
    time.sleep(4)
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_overflowing(browser):
    assert_overflowing(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_ccc_video(browser):
    browser.click(xpath="//div[contains(@class, 'youtube-wrapper')]//div[contains(@class, 'youtube')]")
    e = browser.find(xpath="//div[contains(@class, 'feature-hero-video')]//iframe")
    assert e and e.is_displayed(), 'Video not played'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_video_thumbnail(browser):
    browser.find("//div[contains(@class, 'feature-hero-video')]//img", scroll=True)
    img = browser.find("//div[contains(@class, 'feature-hero-video')]//div[contains(@class, 'youtube')]//img")
    assert img.is_displayed(), 'Video thumbnail image not loaded'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_typography(browser):
    assert_typography(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_customer_logo(browser):
    assert_customer_logo(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_badges(browser):
    assert_badges(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_customer_testimonial(browser):
    assert_customer_testimonial(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email(browser):
    assert_bad_email(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_missing_firstname(browser):
    assert_missing_firstname(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success(browser):
    assert_success(browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_sneak_peek(browser):
    sneak_peak_tabs = browser.find_many("//div[contains(@class, 'tab-section')]//a[contains(@class, 'nav-link')]")
    tabs_checked = 0

    for tab in sneak_peak_tabs:
        browser.hover(tab)
        active_tab = browser.find_many("//div[contains(@class, 'tab-section')]//a[contains(@class, 'nav-link') and contains(@class, 'active')]")
        if (len(active_tab) == 1) and (tab == active_tab[0]):
            tabs_checked += 1
    assert tabs_checked == len(sneak_peak_tabs), 'Error in sneak peek tabs'

# @pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
# def test_cards_url(browser, base_url):
#     urls = [
#         '/travel-expense-management',
#         '/expense-management/expense-analytics',
#         '/expense-policy',
#         '/expense-report-software',
#         '/expense-management'
#     ]

#     arrows = browser.find_many("//section[contains(@class, 'explore-fyle-beyond')]//div[contains(@class, 'feature-blocks')]//a")

#     for i, arrow in enumerate(arrows):
#         browser.find("//section[contains(@class, 'explore-fyle-beyond')]", scroll=True)
#         arrow = browser.find_many("//section[contains(@class, 'explore-fyle-beyond')]//div[contains(@class, 'feature-blocks')]//a")[i]
#         browser.click_element(arrow)
#         assert (base_url + urls[i]) == browser.get_current_url()
#         browser.back()


@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_modal_open(browser):
    browser.click("//section[contains(@class, 'long-background')]//a[contains(@id, 'best-expense-video-id')]")
    modal = browser.find("//div[contains(@id, 'contact-us-modal')]")
    assert modal.is_displayed(), 'Modal is not opened'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_modal_open_bottom(browser):
    browser.click("//section[contains(@class, 'explore-fyle-beyond')]//a[contains(@class, 'new-contact-us-demo-form')]")
    modal = browser.find("//div[contains(@id, 'contact-us-modal')]")
    assert modal.is_displayed(), 'Modal is not opened'
