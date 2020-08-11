import logging
import time
import pytest
from common.utils import resize_browser
from common.asserts import assert_hero_image, assert_typography, assert_customer_logo, assert_overflowing
from common.test_getdemo import assert_bad_email, assert_missing_firstname, assert_success

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/alternative/expensify')
    sleep(2)
    return module_browser

# check for hero image in mobile
@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_hero_image(browser):
    assert_hero_image(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_table(browser):
    section = browser.find(xpath='//section[contains(@class, "alternative-fyle-comparison")]', scroll=True)
    assert section, 'G2 rating table not found'
    divs = browser.find_many(xpath='//div[contains(@class, "accordion-toggle")]')
    num = 1
    for div in divs:
        div_class_names = div.get_attribute('class')
        feature_contents = browser.find(xpath=f'//div[contains(@id, "feature-main-row{num}")]')
        assert feature_contents, 'Feature contents are not present'

        # Check if the feature section is initially collapsed
        # If it's collapsed, then check if it's opening up and it's sub-sections are displayed or not
        # Else it's open, then check if it's collapsing successfully
        if 'accordion-toggle' in div_class_names and 'collapsed' in div_class_names:
            div.click()
            time.sleep(3)
            assert feature_contents.is_displayed(), f'Unable to see contents of feature: {div.text}'
        else:
            div.click()
            time.sleep(3)
            assert feature_contents.is_displayed() is False, f'Unable to collapse feature: {div.text}'
        num += 1
        time.sleep(2)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_typography(browser):
    assert_typography(browser=browser)

# check if the old url is being redirected to the new one
@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_redirection(browser):
    browser.get('https://ww2.fylehq.com/expensify-alternative')
    time.sleep(3)
    current_url = browser.get_current_url()
    assert current_url == 'https://ww2.fylehq.com/alternative/expensify', 'Not redirecting to the right page'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_customer_logo(browser):
    assert_customer_logo(browser=browser)

# check demo form (common section)
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email(browser):
    assert_bad_email(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_missing_firstname(browser):
    assert_missing_firstname(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success(browser):
    assert_success(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_overflowing(browser):
    assert_overflowing(browser=browser)
