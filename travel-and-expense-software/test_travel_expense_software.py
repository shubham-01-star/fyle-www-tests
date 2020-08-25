from time import sleep
import logging
import pytest
from common.utils import resize_browser
from common.asserts import assert_spacing_between, assert_spacing_below, assert_spacing_top, assert_spacing_right, assert_spacing_left
from common.content_download_form import assert_content_download_inline_form, assert_required_fields, assert_invalid_names, assert_bad_email, assert_non_business_email, assert_success_download_form

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/travel-and-expense-software')
    sleep(4)
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_competitor_section_spacing(browser):
    h2 = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//h2")
    underline_dash = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//span[contains(@class, 'underline-dash')]")
    para_text = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//p[contains(@class, 'para-text')]")
    card_list = browser.find_many(xpath="//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]")
    card_sub_text = browser.find_many(xpath="//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(@class, 'paragraph-4--regular')]")
    assert_spacing_between(browser, h2, underline_dash, '60')
    assert_spacing_below(browser, underline_dash, '60')
    assert_spacing_top(browser, para_text, '40')
    assert_spacing_right(browser, para_text, '50')
    for card in card_list:
        assert_spacing_top(browser, card, '30')
        assert_spacing_below(browser, card, '30')
        assert_spacing_right(browser, card, '30')
        assert_spacing_left(browser, card, '30')
    for subtext in card_sub_text:
        assert_spacing_top(browser, subtext, '20')
        assert_spacing_below(browser, subtext, '20')
        assert_spacing_right(browser, subtext, '0')
        assert_spacing_left(browser, subtext, '0')

@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_competitor_section_spacing_mobile(browser):
    h2 = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//h2")
    para_text = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//p[contains(@class, 'para-text')]")
    versus_row = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'versus-row')]")
    card_list = browser.find_many(xpath="//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]")
    card_sub_text = browser.find_many(xpath="//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(@class, 'paragraph-4--regular')]")
    assert_spacing_below(browser, h2, '40')
    assert_spacing_top(browser, para_text, '10')
    assert_spacing_between(browser,para_text, versus_row, '40')
    assert_spacing_between(browser,versus_row, card_list[0],'40')
    for card in card_list:
        assert_spacing_top(browser, card, '20')
        assert_spacing_below(browser, card, '20')
    for subtext in card_sub_text:
        assert_spacing_top(browser, subtext, '15')
        assert_spacing_below(browser, subtext, '15')
        assert_spacing_right(browser, subtext, '0')
        assert_spacing_left(browser, subtext, '0')

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_competitor_section_card_redirection(browser):
    card_url = [
        'https://ww2.fylehq.com/alternative/concur',
        'https://ww2.fylehq.com/alternative/certify',
        'https://ww2.fylehq.com/alternative/expensify',
        'https://ww2.fylehq.com/alternative/chromeriver'
    ]
    card_list = [
        "//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(text(), 'SAP Concur')]//parent::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(text(), 'Certify')]//parent::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(text(), 'Expensify')]//parent::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(text(), 'Chromeriver')]//parent::a"
    ]
    for i, card_xpath in enumerate(card_list):
        card = browser.find(card_xpath, scroll=True)
        browser.click_element(card)
        assert browser.get_current_url() == card_url[i], "redirection url is not correct"
        browser.back()
    
@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_competitor_section_card_redirection_mobile(browser):
    card_url = [
        'https://ww2.fylehq.com/alternative/concur',
        'https://ww2.fylehq.com/alternative/certify',
        'https://ww2.fylehq.com/alternative/expensify',
        'https://ww2.fylehq.com/alternative/chromeriver'
    ]
    card_list = [
        "//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(text(), 'SAP Concur')]/following-sibling::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(text(), 'Certify')]/following-sibling::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(text(), 'Expensify')]/following-sibling::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(text(), 'Chromeriver')]/following-sibling::a"
    ]
    for i, card_xpath in enumerate(card_list):
        card = browser.find(card_xpath, scroll=True)
        browser.scroll_up_or_down(-100)
        browser.click_element(card)
        assert browser.get_current_url() == card_url[i], "redirection url is not correct"
        browser.back()