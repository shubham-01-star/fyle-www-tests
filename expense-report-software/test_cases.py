import logging
from time import sleep
import pytest

from common.utils import resize_browser
from common.asserts import assert_cards_redirection
from common.asserts import assert_cta_click_and_modal_show
from common.asserts import assert_collapsible_feature_comparison_table
from common.asserts import assert_customer_logo
from common.asserts import assert_customer_testimonial
from common.asserts import assert_overflowing
from common.test_getdemo import assert_bad_email
from common.test_getdemo import assert_missing_firstname
from common.test_getdemo import assert_success

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + "/expense-report-software")
    sleep(4)
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_page_overflow(browser):
    assert_overflowing(browser)

# Check demo form (common section)
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
def test_hero_section_cta(browser):
    cta_section_xpath = '//section[contains(@class, "new-hero")]'
    cta_xpath = f'{cta_section_xpath}//div[not(contains(@class, "demo-button-until-banner"))]/a'
    assert_cta_click_and_modal_show(browser, cta_section_xpath, cta_xpath)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_customer_logo_section(browser):
    assert_customer_logo(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_g2_review_table(browser):
    assert_collapsible_feature_comparison_table(browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_customer_testimonial_section(browser):
    assert_customer_testimonial(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bottom_section_cards(browser):
    cards_xpath = '//section[contains(@class, "expense-report-bottom-card-section")]//div[contains(@class, "cards-row")]//div'
    redirect_to_urls = [
        'https://www.youtube.com/watch?v=1UuYrRacA5U',
        'https://ww2.fylehq.com/case-study/3cx-cypress-simplifies-expense-management',
        'https://ww2.fylehq.com/expense-policy/guide',
        'https://ww2.fylehq.com/resources/expense-management-roi-calculator'
    ]
    assert_cards_redirection(browser, cards_xpath, redirect_to_urls)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_bottom_section_cta(browser):
    cta_section_xpath = '//section[contains(@class, "feature-bottom-section")]'
    cta_xpath = f'{cta_section_xpath}//a'
    assert_cta_click_and_modal_show(browser, cta_section_xpath, cta_xpath)
