from time import sleep
import logging
import pytest
from common.utils import resize_browser
from common.asserts import assert_vertical_spacing_between, assert_spacing_bottom, assert_spacing_top, assert_spacing_right, assert_spacing_left, assert_overflowing, assert_customer_testimonial, assert_customer_logo, assert_typography, assert_cards_redirection

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/expense-management-software')
    sleep(4)
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_page_overflow(browser):
    assert_overflowing(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_typography(browser):
    assert_typography(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_customer_logo(browser):
    assert_customer_logo(browser=browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_competitor_section_spacing(browser):
    section = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]")
    h2 = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//h2")
    underline_dash = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//span[contains(@class, 'underline-dash')]")
    para_text = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//p[contains(@class, 'para-text')]")
    card_list = browser.find_many(xpath="//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]")
    card_sub_text = browser.find_many(xpath="//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(@class, 'paragraph-4--regular')]")
    assert_spacing_top(section, 80)
    assert_spacing_bottom(section, 80)
    assert_vertical_spacing_between(h2, underline_dash, 60)
    assert_spacing_bottom(underline_dash, 60)
    assert_spacing_top(para_text, 40)
    assert_spacing_right(para_text, 50)
    for card in card_list:
        assert_spacing_top(card, 30)
        assert_spacing_bottom(card, 30)
        assert_spacing_right(card, 30)
        assert_spacing_left(card, 30)
    for subtext in card_sub_text:
        assert_spacing_top(subtext, 20)
        assert_spacing_bottom(subtext, 20)
        assert_spacing_right(subtext, 0)
        assert_spacing_left(subtext, 0)

@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_competitor_section_spacing_mobile(browser):
    section = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]")
    h2 = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//h2")
    para_text = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//p[contains(@class, 'para-text')]")
    versus_row = browser.find(xpath="//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'versus-row')]")
    card_list = browser.find_many(xpath="//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]")
    card_sub_text = browser.find_many(xpath="//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(@class, 'paragraph-4--regular')]")
    assert_spacing_top(section, 40)
    assert_spacing_bottom(section, 20)
    assert_spacing_bottom(h2, 40)
    assert_spacing_top(para_text, 10)
    assert_vertical_spacing_between(para_text, versus_row, 40)
    assert_vertical_spacing_between(versus_row, card_list[0], 40)
    for card in card_list:
        assert_spacing_top(card, 20)
        assert_spacing_bottom(card, 20)
    for subtext in card_sub_text:
        assert_spacing_top(subtext, 15)
        assert_spacing_bottom(subtext, 15)
        assert_spacing_right(subtext, 0)
        assert_spacing_left(subtext, 0)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_competitor_section_card_redirection(browser):
    card_url = [
        'https://ww2.fylehq.com/alternative/concur',
        'https://ww2.fylehq.com/alternative/certify',
        'https://ww2.fylehq.com/alternative/expensify',
        'https://ww2.fylehq.com/alternative/chromeriver'
    ]
    card_list_desktop = [
        "//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(text(), 'SAP Concur')]//parent::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(text(), 'Certify')]//parent::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(text(), 'Expensify')]//parent::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//a[contains(@class, 'competitor-cards')]//p[contains(text(), 'Chrome River')]//parent::a"
    ]
    card_list_mobile = [
        "//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(text(), 'SAP Concur')]/following-sibling::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(text(), 'Certify')]/following-sibling::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(text(), 'Expensify')]/following-sibling::a",
        "//section[contains(@class, 'fyle-vs-competitors')]//div[contains(@class, 'competitor-cards')]//p[contains(text(), 'Chrome River')]/following-sibling::a"
    ]
    if browser.is_desktop():
        card_list = card_list_desktop
    else:
        card_list = card_list_mobile
    
    assert_cards_redirection(browser, card_list, card_url, same_tab=True)
