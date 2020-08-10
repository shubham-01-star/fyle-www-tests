import time
import logging
import pytest

from common.asserts import assert_customer_logo
from common.asserts import assert_badges
from common.asserts import assert_customer_testimonial
from common.asserts import assert_typography
from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/corporate-credit-cards')
    time.sleep(3)
    return module_browser

#common utils

def check_spacing(element_1, element_2, space):
    element_1_Y = element_1.location['y']
    element_2_Y = element_2.location['y']
    element_1_height = element_1.size['height']
    space_difference = abs(element_1_Y - element_2_Y) - element_1_height
    return space_difference == space


def padding_bottom_of(element, value):
    return element.value_of_css_property('padding-bottom') == value


def padding_top_of(element, value):
    return element.value_of_css_property('padding-top') == value


def margin_top_of(element, value):
    return element.value_of_css_property('margin-top') == value


def margin_bottom_of(element, value):
    return element.value_of_css_property('margin-bottom') == value


def padding_of(element, value):
    return element.value_of_css_property('padding') == value


def margin_of(element, value):
    return element.value_of_css_property('margin') == value


#end of common utils
@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_ccc_video(browser):
    time.sleep(1)
    browser.click(xpath="//div[contains(@class, 'youtube-wrapper')]//div[contains(@class, 'youtube')]")
    time.sleep(5)
    e = browser.find(xpath="//div[contains(@class, 'feature-hero-video')]//iframe")
    assert e and e.is_displayed(), 'Video not played'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_video_thumbnail(browser):
    browser.find("//div[contains(@class, 'feature-hero-video')]//img", scroll=True)
    time.sleep(2)
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

    #Checking spacing between tabs
    for i in range(len(sneak_peak_tabs) - 1):
        assert check_spacing(sneak_peak_tabs[i], sneak_peak_tabs[i+1], 30)


@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_h1_subtext(browser):
    h1 = browser.find("//section[contains(@class, 'long-background')]//h1[contains(@class, 'heading-primary')]")
    subtext = browser.find("//section[contains(@class, 'long-background')]//p[contains(@class, 'sub-text')]")
    assert check_spacing(h1, subtext, 20), 'H1 and subtest spacing wrong'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_subtext_button(browser):
    subtext = browser.find("//section[contains(@class, 'long-background')]//p[contains(@class, 'sub-text')]")
    button = browser.find("//section[contains(@class, 'long-background')]//a[contains(@id, 'best-expense-video-id')]")
    assert check_spacing(subtext, button, 40), 'Subtext and button spacing wrong'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_h3_subtext(browser):
    h3 = browser.find_many("//section[contains(@class, 'long-background')]//div[contains(@class, 'feature-pages-solution')]//h3")
    subtext = browser.find_many("//section[contains(@class, 'long-background')]//div[contains(@class, 'feature-pages-solution')]//p")

    for i, h3 in enumerate(h3):
        assert check_spacing(h3, subtext[i], 10), 'Spacing between h3 and subtext is wrong'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_h2_logo(browser):
    h2 = browser.find("//section[contains(@class, 'customer-logos-v2')]//div[contains(@class, 'col')]//h2")
    logo = browser.find("//section[contains(@class, 'customer-logos-v2')]//div[contains(@class, 'col')]//div[not(contains(@class, 'd-none'))]")
    assert check_spacing(h2, logo, 40), 'Spacing between h2 and logo is wrong'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_cards_url(browser, base_url):
    links = []
    urls = [
        '/travel-expense-management',
        '/expense-management/expense-analytics',
        '/expense-policy',
        '/expense-report-software',
        '/expense-management'
    ]
    cards = browser.find_many("//section[contains(@class, 'explore-fyle-beyond')]//div[contains(@class, 'feature-blocks')]//a")

    for i, card in enumerate(cards):
        links.append(card.get_attribute('href'))

    for i, link in enumerate(links):
        browser.get(link)
        assert (base_url + urls[i]) == browser.get_current_url()
        browser.back()

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_modal_open(browser):
    browser.click("//section[contains(@class, 'long-background')]//a[contains(@id, 'best-expense-video-id')]")
    time.sleep(3)
    modal = browser.find("//div[contains(@id, 'contact-us-modal')]")
    assert modal.is_displayed(), 'Modal is not opened'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_modal_open_bottom(browser):
    browser.click("//section[contains(@class, 'explore-fyle-beyond')]//a[contains(@class, 'new-contact-us-demo-form')]")
    time.sleep(3)
    modal = browser.find("//div[contains(@id, 'contact-us-modal')]")
    assert modal.is_displayed(), 'Modal is not opened'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_sneak_peek_bottom_features(browser):
    icons = browser.find_many("//div[contains(@class, 'info-box')]//div[contains(@class, 'pic')]")
    headings = browser.find_many("//div[contains(@class, 'info-box')]//div[contains(@class, 'heading')]")

    for i, icon in enumerate(icons):
        assert padding_bottom_of(icon, '10px'), 'Icon padding is incorrect.'
        assert padding_bottom_of(headings[i], '10px'), 'Heading padding is incorrect.'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_travel_benefits(browser):
    travel_benefits_row = browser.find("//div[contains(@class, 'travel-request-benefits')]")
    row_padding_top = travel_benefits_row.value_of_css_property('padding-top')
    row_padding_bottom = travel_benefits_row.value_of_css_property('padding-bottom')
    assert row_padding_top == '50px' and row_padding_bottom == '45px', f'Padding top or bottom is incorrect, the correct values are 50px top and 45px bottom, but {row_padding_top} and {row_padding_bottom} found'


@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_feature_solution(browser):
    feature_solution_row = browser.find("//div[contains(@class, 'feature-pages-solution')]")
    row_padding_top = feature_solution_row.value_of_css_property('padding-top')
    assert row_padding_top == '40px', f'Padding top is incorrect, the correct value is 40px, but {row_padding_top} found'


@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_hero_margin_top(browser):
    hero = browser.find("//section[contains(@class, 'feature-pages-hero')]")
    hero_container = browser.find("//section[contains(@class, 'feature-pages-hero')]//div")
    assert margin_top_of(hero, '30px') and margin_top_of(hero_container, '80px'), 'Margin top of hero is incorrect'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_logo_padding(browser):
    section = browser.find("//section[contains(@class, 'customer-logos-v2')]")
    assert padding_bottom_of(section, '80px'), 'Padding bottom of logo section is wrong'
    assert padding_top_of(section, '40px'), 'Padding top of log section is wrong'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_logo_h2(browser):
    h2 = browser.find("//section[contains(@class, 'customer-logos-v2')]//h2")
    assert margin_bottom_of(h2, '40px'), 'Margin bottom of logo h2 is wrong'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_sneak_peek_h2(browser):
    h2 = browser.find("//section[contains(@class, 'software-sneak-peek-section')]//h2")
    assert margin_bottom_of(h2, '20px') and padding_bottom_of(h2, '20px'), 'Margin or padding bottom of h2 is wrong'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_logo_space_h2(browser):
    h2 = browser.find("//div[contains(@class, 'testimonial-heading')]//h2")
    assert padding_bottom_of(h2, '10px')
    subtext = browser.find("//div[contains(@class, 'testimonial-heading')]//p")
    assert margin_bottom_of(subtext, '40px')

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_card_h2(browser):
    h2 = browser.find("//section[contains(@class, 'explore-fyle-beyond')]//h2")
    assert padding_bottom_of(h2, '20px')

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_hero_space(browser):
    hero = browser.find("//section[contains(@class, 'feature-pages-hero')]")
    assert margin_top_of(hero, '30px'), 'Margin top of hero is wrong'
    assert padding_of(hero, '40px 0px'), 'Padding of hero section is wrong'


@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_space_logo_section(browser):
    section = browser.find("//section[contains(@class, 'customer-logos-v2')]")
    assert padding_top_of(section, '40px') and padding_bottom_of(section, '80px'), 'Padding of logo section is wrong'

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_padding_sneak_peek(browser):
    section = browser.find("//section[contains(@class, 'software-sneak-peek-section')]")
    assert padding_of(section, '40px 0px')

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_badges_padding(browser):
    section = browser.find("//section[contains(@class, 'fyle-recognition-badges ')]")
    assert padding_of(section, '40px 0px')

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_testimonial_padding(browser):
    section = browser.find("//section[contains(@class, 'customer-testimonial')]")
    assert padding_of(section, '80px 0px 134px')

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_explore_features_padding(browser):
    section = browser.find("//section[contains(@class, 'explore-fyle-beyond')]")
    assert padding_of(section, '40px 0px') and margin_top_of(section, '40px')
