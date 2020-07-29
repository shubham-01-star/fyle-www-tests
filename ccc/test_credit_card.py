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

#common utils

def check_spacing(element_1, element_2, space):
    element_1_Y = element_1.location['y']
    element_2_Y = element_2.location['y']
    element_1_height = element_1.size['height']
    element_2_height = element_2.size['height']
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


#end of common utils

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

    #Checking spacing between tabs
    for i in range(len(sneak_peak_tabs) - 1):
        assert check_spacing(sneak_peak_tabs[i], sneak_peak_tabs[i+1], 30)


def test_space_h1_subtext(browser):
    h1 = browser.find("//section[contains(@class, 'long-background')]//h1[contains(@class, 'heading-primary')]")
    subtext = browser.find("//section[contains(@class, 'long-background')]//p[contains(@class, 'sub-text')]")
    assert check_spacing(h1, subtext, 20), 'H1 and subtest spacing wrong'


def test_space_subtext_button(browser):
    subtext = browser.find("//section[contains(@class, 'long-background')]//p[contains(@class, 'sub-text')]")
    button = browser.find("//section[contains(@class, 'long-background')]//a[contains(@id, 'best-expense-video-id')]")
    assert check_spacing(subtext, button, 40), 'Subtext and button spacing wrong'


def test_space_h3_subtext(browser):
    h3 = browser.find_many("//section[contains(@class, 'long-background')]//div[contains(@class, 'feature-pages-solution')]//h3")
    subtext = browser.find_many("//section[contains(@class, 'long-background')]//div[contains(@class, 'feature-pages-solution')]//p")

    for i in range(len(h3)):
        assert check_spacing(h3[i], subtext[i], 10), 'Spacing between h3 and subtext is wrong'


def test_space_h2_logo(browser):
    h2 = browser.find("//section[contains(@class, 'customer-logos-v2')]//div[contains(@class, 'col')]//h2")
    logo = browser.find("//section[contains(@class, 'customer-logos-v2')]//div[contains(@class, 'col')]//div[not(contains(@class, 'd-none'))]")
    assert check_spacing(h2, logo, 40), 'Spacing between h2 and logo is wrong'


def test_cards_url(browser):
    links = []
    urls = [
        'https://ww2.fylehq.com/travel-expense-management',
        'https://ww2.fylehq.com/expense-management/expense-analytics',
        'https://ww2.fylehq.com/expense-policy',
        'https://ww2.fylehq.com/expense-report-software',
        'https://ww2.fylehq.com/expense-management'
    ]
    cards = browser.find_many("//section[contains(@class, 'explore-fyle-beyond')]//div[contains(@class, 'feature-blocks')]//a")

    for i in range(len(cards)):
        links.append(cards[i].get_attribute('href'))

    for i in range(len(links)):
        browser.get(links[i])
        assert urls[i] == browser.get_current_url()
        browser.back()


def test_modal_open(browser):
    cta = browser.click("//section[contains(@class, 'long-background')]//a[contains(@id, 'best-expense-video-id')]")
    modal = browser.find("//div[contains(@id, 'contact-us-modal') and contains(@style, 'display: block;')]")
    assert modal, 'Modal is not opened'


def test_modal_open_bottom(browser):
    cta = browser.find_by_css(".explore-fyle-beyond .container:last-child").click()
    modal = browser.find("//div[contains(@id, 'contact-us-modal') and contains(@style, 'display: block;')]")
    assert modal, 'Modal is not opened'


def test_sneak_peek_bottom_features(browser):
    icons = browser.find_many("//div[contains(@class, 'info-box')]//div[contains(@class, 'pic')]")
    headings = browser.find_many("//div[contains(@class, 'info-box')]//div[contains(@class, 'heading')]")

    for i in range(len(icons)):
        icon_padding = icons[i].value_of_css_property('padding-bottom')
        heading_padding = headings[i].value_of_css_property('padding-bottom')
        assert icon_padding == '10px', f'Icon padding is incorrect, the correct value is 10px but {icon_padding} found'
        assert heading_padding == '10px', f'Heading padding is incorrect, the correct value is 10px but {heading_padding} found'


def test_space_travel_benefits(browser):
    travel_benefits_row = browser.find("//div[contains(@class, 'travel-request-benefits')]")
    row_padding_top = travel_benefits_row.value_of_css_property('padding-top')
    row_padding_bottom = travel_benefits_row.value_of_css_property('padding-bottom')
    assert row_padding_top == '50px' and row_padding_bottom == '45px', f'Padding top or bottom is incorrect, the correct values are 50px top and 45px bottom, but {row_padding_top} and {row_padding_bottom} found'


def test_space_feature_solution(browser):
    feature_solution_row = browser.find("//div[contains(@class, 'feature-pages-solution')]")
    row_padding_top = feature_solution_row.value_of_css_property('padding-top')
    assert row_padding_top == '40px', f'Padding top is incorrect, the correct value is 40px, but {row_padding_top} found'


def test_hero_margin_top(browser):
    hero = browser.find("//section[contains(@class, 'feature-pages-hero')]")
    hero_container = browser.find("//section[contains(@class, 'feature-pages-hero')]//div")
    margin_hero = hero.value_of_css_property('margin-top')
    margin_container = hero.value_of_css_property('margin-top')
    assert maring_hero == '30px', 'Margin top of hero is incorrect'
    assert margin_container == '80px', 'Margin top of container is incorrect'

def test_logo_padding(browser):
    section = browser.find("//section[contains(@class, 'customer-logos-v2')]")
    assert padding_bottom_of(section, '80px'), 'Padding bottom of logo section is wrong'
    assert padding_top_of(section, '40px'), 'Padding top of log section is wrong'


def test_space_logo_h2(browser):
    h2 = browser.find("//section[contains(@class, 'customer-logos-v2')]//h2")
    assert margin_bottom_of(h2, '40px'), 'Margin bottom of logo h2 is wrong'


def test_space_sneak_peek_h2(browser):
    h2 = browser.find("//section[contains(@class, 'software-sneak-peek-section')]//h2")
    assert margin_bottom_of(h2, '20px') and padding_bottom_of(h2, '20px'), 'Margin or padding bottom of h2 is wrong'


def test_space_logo_h2(browser):
    h2 = browser.find("//div[contains(@class, 'testimonial-heading')]//h2")
    assert padding_bottom_of(h2, '10px')
    subtext = browser.find("//div[contains(@class, 'testimonial-heading')]//p")
    assert margin_bottom_of(subtext, '40px')


def test_space_card_h2(browser):
    h2 = browser.find("//section[contains(@class, 'explore-fyle-beyond')]//h2")
    assert padding_bottom_of(h2, '20px')