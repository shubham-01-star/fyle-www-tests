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

def assert_content_download_thank_you_page(browser, title, email, content_url):
    url = browser.get_current_url()
    assert '/thank-you' in url, "Thank you page is not displayed"
    page_title = browser.find(xpath="//section[contains(@class, 'resource-thank-you')]//span[contains(@class, 'thank-you-page-title')]").text
    assert title == page_title, "Content title is not correct"
    user_email = browser.find(xpath="//section[contains(@class, 'resource-thank-you')]//span[contains(@class, 'thank-you-page-email')]").text
    assert email == user_email, "User email is not correct"
    url_link = browser.find(xpath="//section[contains(@class, 'resource-thank-you')]//a[contains(@id, 'download-link')]")
    url_link.click()
    browser.switch_tab_next(1)
    time.sleep(2)
    assert browser.get_current_url() == content_url, "Content download link is correct"
    browser.close_windows()
    random_cards = browser.find_many(xpath="//section[contains(@class, 'random-card-section')]//a//h4")
    for i, resource in enumerate(random_cards):
        time.sleep(2)
        assert resource.text != title, "Random cards are not properly generated"
