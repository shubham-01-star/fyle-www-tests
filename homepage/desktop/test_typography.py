import time
from simplebrowser import SimpleBrowser
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture
def browser(module_browser, base_url):
    assert module_browser.is_desktop(), 'this test can only be run on desktops'
    module_browser.get(base_url)
    return module_browser

def test_hero_section(browser):
    sections = browser.find_many(xpath='//section')
    section = sections[0]
    h1s = section.find_elements_by_xpath('.//h1')
    assert len(h1s) == 1, 'Hero section should have 1 h1'
    h2s = section.find_elements_by_xpath('.//h2')
    assert len(h2s) == 0, 'Hero section should have no h2s'

def test_other_sections(browser):
    sections = browser.find_many(xpath='//section')[1:]
    for section in sections:
        cl = section.get_attribute('class')
        h2s = section.find_elements_by_xpath('.//h2')
        assert len(h2s) == 1, f'Section with class {cl} has {len(h2s)} h2s'

def test_h2_font(browser):
    h2s = browser.find_many(xpath='//h2')
    for h2 in h2s:
        text = h2.text
        font_size = h2.value_of_css_property('font-size')
        font_weight = h2.value_of_css_property('font-weight')
#        logger.info('checking h2 %s, font-size %s', text, font_size)
        if 'Loved by leading finance' in h2.text:
            assert font_size == '24px', 'Font size of logo section is wrong'
        else:
            assert font_size == '30px', f'Font size of h2 is wrong for {text}'
        assert font_weight == '700', f'Font weight of h2 is wrong for {text}'