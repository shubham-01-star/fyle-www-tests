import time
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
    time.sleep(3)
    indian_logo = browser.find("//div[contains(@class, 'customer-logo-india')]")
    us_logo = browser.find("//div[contains(@class, 'customer-logo-non-india')]")
    assert indian_logo.is_displayed() and not us_logo.is_displayed(), 'Found an US image in Indian IP'

    browser.set_storage('ipInfo', '{"ip":"157.50.160.253","country":"United States"}')
    browser.refresh()
    time.sleep(3)
    indian_logo = browser.find("//div[contains(@class, 'customer-logo-india')]")
    us_logo = browser.find("//div[contains(@class, 'customer-logo-non-india')]")
    assert us_logo.is_displayed() and not indian_logo.is_displayed(), 'Found an Indian image in US IP'

def assert_badges(browser):
    total_badges = browser.find_many("//div[contains(@class, 'fyle-badge')]")
    visible_badge = 0
    for badge in total_badges:
        if badge.is_displayed():
            visible_badge += 1
    assert visible_badge == 1, 'Badges aren\'t displayed properly.'


def get_active_index(carousel_items):
    active_item = []
    for i, item in enumerate(carousel_items):
        if "active" in item.get_attribute("class"):
            active_item.append(item)
            active_index = i
    no_of_active_items = len(active_item)
    assert no_of_active_items != 0 and no_of_active_items <= 1, 'UI broken in customer testimonial section'
    return active_index

def assert_customer_testimonial(browser):
    time.sleep(3)
    carousel_items = browser.find_many("//div[contains(@class, 'carousel-item')]")
    carousel_length = len(carousel_items)
    current_active_index = get_active_index(carousel_items)

    time.sleep(1)
    browser.force_click(xpath="//div[contains(@id, 'customer-carousel')]//a[contains(@class, 'right')]")
    time.sleep(1)
    active_index = get_active_index(carousel_items)
    assert active_index == ((current_active_index + 1) % carousel_length), 'Right click operation is not working'

    browser.refresh()
    time.sleep(1)
    carousel_items = browser.find_many("//div[contains(@class, 'carousel-item')]")
    time.sleep(1)
    browser.force_click(xpath="//div[contains(@id, 'customer-carousel')]//a[contains(@class, 'left')]")
    time.sleep(1)
    active_index = get_active_index(carousel_items)
    assert active_index == ((current_active_index + (carousel_length - 1)) % carousel_length), 'Left click operation is not working'
