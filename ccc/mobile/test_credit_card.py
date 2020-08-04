import os
import time
from simplebrowser import SimpleBrowser
import logging
import pytest
from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    module_browser.get(base_url + '/corporate-credit-cards')
    return module_browser


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


def padding_of(element, value):
	return element.value_of_css_property('padding') == value


def margin_of(element, value):
	return element.value_of_css_property('margin') == value


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_space_h3_subtext(browser):
    h3 = browser.find_many("//section[contains(@class, 'long-background')]//div[contains(@class, 'feature-pages-solution')]//h3")
    subtext = browser.find_many("//section[contains(@class, 'long-background')]//div[contains(@class, 'feature-pages-solution')]//p")

    for i in range(len(h3)):
        assert check_spacing(h3[i], subtext[i], 10), 'Spacing between h3 and subtext is wrong'


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_space_travel_benefits(browser):
    travel_benefits_row = browser.find("//div[contains(@class, 'travel-request-benefits')]")
    assert padding_top_of(travel_benefits_row, '40px') and padding_bottom_of(row_padding_bottom, '20px'), 'Padding top or bottom is wrong'


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_space_benefit_text(browser):
	benefit_texts = browser.find_many("//p[contains(@class, 'benefit-text')]")
	for text in benefit_texts:
		assert margin_top_of(text, '5px') and margin_bottom_of(text, '20px'), 'Marign values of benefit text is wrong'


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_space_feature_solution(browser):
    feature_solution_row = browser.find("//div[contains(@class, 'feature-pages-solution')]")
    assert padding_top_of(feature_solution_row, '30px'), f'Padding top is incorrect, the correct value is 30px, but {row_padding_top} found'


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_space_logo(browser):
	section = browser.find("//div[contains(@class, 'logo-section')]")
	assert padding_of(section, '40px 42px')


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_space_sneak_peek(browser):
	cards = browser.find_many("//div[contains(@class, 'card-section')]")
	headings = browser.find_many("//div[contains(@class, 'card-section')]//p[contains(@class, 'heading')]")
	descriptions = browser.find_many("//div[contains(@class, 'card-section')]//p[contains(@class, 'description')]")
	
	for i in range(len(cards)):
		assert margin_bottom_of(cards[i], '20px'), 'Margin bottom of card is wrong'
		assert padding_of(headings[i], '20px 20px 10px'), 'Padding values of heading is wrong'
		assert padding_of(descriptions[i], '0px 20px 20px'), 'Padding values of description is wrong'


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_space_logo_h2(browser):
    h2 = browser.find("//div[contains(@class, 'testimonial-heading')]//h2")
    assert margin_bottom_of(h2, '20px')
    subtext = browser.find("//div[contains(@class, 'testimonial-heading')]//p")
    assert margin_bottom_of(subtext, '30px')


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_hero_space(browser):
	hero = browser.find("//section[contains(@class, 'feature-pages-hero')]")
	assert margin_top_of(hero, '30px'), 'Margin top of hero is wrong'
	assert padding_of(hero, '25px 0px'), 'Padding of hero section is wrong'


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_space_logo_section(browser):
	section = browser.find("//section[contains(@class, 'customer-logos-v2')]")
	assert padding_top_of(section, '25px') and padding_bottom_of(section, '80px'), 'Padding of logo section is wrong'


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_padding_sneak_peek(browser):
	section = browser.find("//section[contains(@class, 'software-sneak-peek-section')]")
	assert padding_of(section, '25px 0px')


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_badges_padding(browser):
	section = browser.find("//section[contains(@class, 'fyle-recognition-badges ')]")
	assert padding_of(section, '25px 0px')


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_testimonial_padding(browser):
	section = browser.find("//section[contains(@class, 'customer-testimonial')]")
	assert padding_of(section, '40px 0px 80px')


@pytest.mark.parametrize('browser', [('mobile_1')], indirect=True)
def test_explore_features_padding(browser):
	section = browser.find("//section[contains(@class, 'explore-fyle-beyond')]")
	assert padding_of(section, '25px 0px') and margin_of(section, '25px 0px')


