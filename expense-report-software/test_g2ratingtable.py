from time import sleep
import logging
import pytest

from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + "/expense-report-software")
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_table(browser):
    section = browser.find(xpath='//section[contains(@class, "alternative-fyle-comparison")]', scroll=True)
    assert section, 'G2 rating table not found'
    divs = browser.find_many(xpath='//div[contains(@class, "accordion-toggle")]')
    num = 1
    for div in divs:
        div_class_names = div.get_attribute('class')
        feature_contents = browser.find(xpath=f'//div[contains(@id, "feature-main-row{num}")]')
        assert feature_contents, 'Feature contents are not present'
        if 'accordion-toggle' in div_class_names and 'collapsed' in div_class_names:
            div.click()
            sleep(3)
            assert feature_contents.is_displayed(), f'Unable to see contents of feature: {div.text}'
        else:
            div.click()
            sleep(3)
            assert feature_contents.is_displayed() is False, f'Unable to collapse feature: {div.text}'
        num += 1
        sleep(2)
