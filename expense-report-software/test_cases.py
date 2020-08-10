from time import sleep
import logging
import pytest

from common.utils import resize_browser
from common.asserts import assert_cards_redirection, assert_cta_click_and_modal_show

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + "/expense-report-software")
    return module_browser

#OTHER TEST CASES WHICH ARE REQUIRED TO BE ADDED HERE
#- Hero section cta check
#- Company logos section
#- Testimonial section

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

        # Check if the feature section is initially collapsed
        # If it's collapsed, then check if it's opening up and it's sub-sections are displayed or not
        # Else it's open, then check if it's collapsing successfully
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

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bottom_section_cards(browser):
    cards = browser.find_many(xpath='//section[contains(@class, "expense-report-bottom-card-section")]//div[contains(@class, "cards-row")]//div')
    redirect_to_urls = [
        'https://www.youtube.com/watch?v=1UuYrRacA5U',
        'https://ww2.fylehq.com/case-study/3cx-cypress-simplifies-expense-management',
        'https://ww2.fylehq.com/expense-policy/guide',
        'https://ww2.fylehq.com/resources/expense-management-roi-calculator'
    ]
    assert_cards_redirection(browser, cards, redirect_to_urls)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_bottom_section_cta(browser):
    cta_xpath = '//section[contains(@class, "feature-bottom-section")]//a'
    assert_cta_click_and_modal_show(browser, cta_xpath)
