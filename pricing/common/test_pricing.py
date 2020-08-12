import logging
import time
import pytest
from common.utils import resize_browser
from common.asserts import assert_customer_testimonial, assert_overflowing
from common.test_getdemo import assert_bad_email, assert_missing_firstname, assert_success

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + "/pricing")
    time.sleep(4)
    return module_browser

# # check demo form (common section)
# @pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
# def test_bad_email(browser):
#     assert_bad_email(browser)

# @pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
# def test_missing_firstname(browser):
#     assert_missing_firstname(browser)

# @pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
# def test_success(browser):
#     assert_success(browser)

# # check slide change in cutsomer testimonial (common section)
# @pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
# def test_customer_testimonial(browser):
#     assert_customer_testimonial(browser=browser)

# # check page x-overflow (common method)
# @pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
# def test_overflowing(browser):
#     assert_overflowing(browser)

# # check pricing page is redirecting to bcp page
# @pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
# def test_bcp_redirection(browser):
#     browser.click(xpath="//a[contains(text(), 'Click here')]")
#     assert browser.get_current_url() == 'https://ww2.fylehq.com/business-continuity-plan-covid-19', 'Redirection to bcp failed'
#     browser.back()

# check all 3 pricing cards have cta which open demo form (exit intent opening error)
@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_cards_cta(browser):
    card_ctas = browser.find_many("//div[contains(@class, 'card-footer')]")
    close_form = browser.find("//button[contains(@class, 'close')]")
    demo_form = browser.find(xpath="//form[@id='contact-us-form']")
    for i, cta in enumerate(card_ctas):
        browser.click_element(cta)
        assert demo_form and demo_form.is_displayed(), f'Demo form is not opening in card no. {i}'
        browser.click_element(close_form)

# check toggle of compare plans table
@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_compareplan_table(browser):
    table = browser.find(xpath="//div[contains(@class, 'feature-table')]")
    assert table and table.is_displayed() is False, 'Compare all plans table is already open, by default'
    # scrolling so that element is not hidden behind sticky cta
    browser.find(xpath="//a[@id='show-hide-enterprise']", scroll=True)
    browser.click(xpath="//button[contains(text(), 'Compare all plans')]")
    assert table and table.is_displayed(), 'Compare all plans table is not opening'

# check the ctas present inside the compare all plans table
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_download_cta(browser):
    open_table_btn = browser.find(xpath="//button[contains(text(), 'Compare all plans')]", scroll=True)
    browser.scroll_down(-200)
    browser.click_element(open_table_btn)
    cta = browser.find(xpath="//button[contains(text(), 'Download all plans')]", scroll=True)
    browser.scroll_down(-200)
    browser.click_element(cta)
    download_form = browser.find(xpath="//form[@id='contact-us-form-feature-download']")
    assert download_form and download_form.is_displayed(), 'All feature download form is not open'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_demo_cta(browser):
    browser.click(xpath="//button[contains(text(), 'Compare all plans')]")
    browser.click(xpath="//div[contains(@class, 'compare-all-cta')]//button[contains(text(), 'Get a demo')]")
    demo_form = browser.find(xpath="//form[@id='contact-us-form']")
    assert demo_form and demo_form.is_displayed(), 'Demo form is not open'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_scroll_top(browser):
    open_table_btn = browser.find(xpath="//button[contains(text(), 'Compare all plans')]", scroll=True)
    browser.scroll_down(-200)
    browser.click_element(open_table_btn)
    browser.scroll_down(100)
    browser.click(xpath="//a[contains(@class, 'scroll-top-arrow')]")
    business_pricing_card = browser.find(xpath="//h2[contains(@class, 'card-title') and contains(text(), 'Business')]")
    assert business_pricing_card.is_displayed(), 'Scroll top is not scrolling to the desired section'

# check FAQ collapsibles
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_collapsible_faq(browser):
    faq_answer = browser.find(xpath="//div[@id='faq-1-content']", scroll=True)
    assert faq_answer.is_displayed() is False, 'FAQ answer is not collapsed by default'
    faq_question = browser.find(xpath="//div[@id='faq-1-heading']", scroll=True)
    browser.scroll_down(-200)
    browser.click_element(faq_question)
    assert faq_answer.is_displayed(), 'FAQ answer is not opening on click'
    browser.click(xpath="//div[@id='faq-1-heading']")
    # sleep required for transition/closing of collapsible
    time.sleep(2)
    assert faq_answer.is_displayed() is False, 'FAQ answer is not collapsing on click'

# check table header for compare all plans is sticky or not
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_sticky_table_header(browser):
    open_table_btn = browser.find(xpath="//button[contains(text(), 'Compare all plans')]", scroll=True)
    browser.scroll_down(-200)
    browser.click_element(open_table_btn)
    browser.find(xpath="//div[contains(@class, 'table-data') and contains(text(), 'Real-time Policy Violations')]", scroll=True)
    header_position = browser.find(xpath="//div[contains(@class, 'table-head')]")
    assert header_position.value_of_css_property('position') == 'sticky', 'Compare all plans table header is not sticky'

# check collapsible pricing card details in mobile
@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_collapsible_details(browser):
    see_details = browser.find(xpath="//a[@id='show-hide-standard']", scroll=True)
    # scrolling up so that element is not hidden behind navbar
    browser.scroll_down(-100)
    browser.click_element(see_details)
    details = browser.find(xpath="//div[@id='standard-collapse']")
    assert details and details.is_displayed(), 'Show details is not opening the collapsible'
