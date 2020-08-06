import logging

logger = logging.getLogger(__name__)

def assert_hero_section(browser, section):
    h1s = section.find_elements_by_xpath('.//h1')
    assert len(h1s) == 1, 'Hero section should have 1 h1'
    h1 = h1s[0]
    font_size = h1.value_of_css_property('font-size')
    if browser.is_desktop():
        assert font_size == '50px', 'Hero section h1 font size is wrong'
    else:
        assert font_size == '30px', 'Hero section h1 font size is wrong'
    h2s = section.find_elements_by_xpath('.//h2')
    assert len(h2s) == 0, 'Hero section should have no h2s'


def assert_other_section(browser, section):
    cl = section.get_attribute('class')
    h2s = section.find_elements_by_xpath('.//h2')
    assert len(h2s) == 1, f'Section with class {cl} has {len(h2s)} h2s'
    h2 = h2s[0]
    text = h2.text
    font_size = h2.value_of_css_property('font-size')
    font_weight = h2.value_of_css_property('font-weight')
    is_logo_section = 'Loved by leading finance' in text
    if browser.is_desktop():
        if is_logo_section:
            assert font_size == '24px', 'Font size of logo section is wrong'
        else:
            assert font_size == '30px', f'Font size of h2 is wrong for {text}'
    else:
        if is_logo_section:
            assert font_size == '16px', 'Font size of logo section is wrong'
        else:
            assert font_size == '24px', f'Font size of h2 is wrong for {text}'
    assert font_weight == '700', f'Font weight of h2 is wrong for {text}'

def assert_typography(browser):
    sections = browser.find_many(xpath='//section')
    hero_section = sections[0]
    other_sections = sections[1:]
    assert_hero_section(browser=browser, section=hero_section)
    for other_section in other_sections:
        assert_other_section(browser=browser, section=other_section)

def assert_customer_logo(browser):
    browser.set_storage('ipInfo', '{"ip":"157.50.160.253","country":"India"}')
    browser.refresh()
    indian_logo = browser.find("//div[contains(@class, 'customer-logo-india')]")
    us_logo = browser.find("//div[contains(@class, 'customer-logo-non-india')]")
    assert indian_logo.is_displayed() and not us_logo.is_displayed(), 'Found an US image in Indian IP'

    browser.set_storage('ipInfo', '{"ip":"157.50.160.253","country":"United States"}')
    browser.refresh()
    indian_logo = browser.find("//div[contains(@class, 'customer-logo-india')]")
    us_logo = browser.find("//div[contains(@class, 'customer-logo-non-india')]")
    assert us_logo.is_displayed() and not indian_logo.is_displayed(), 'Found an Indian image in US IP'
