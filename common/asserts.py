from time import sleep
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

def assert_collapsible_feature_comparison_table(browser):
    section = browser.find(xpath='//section[contains(@class, "alternative-fyle-comparison")]', scroll=True)
    assert section, 'Collapsible table not found'
    divs = browser.find_many(xpath='//div[contains(@class, "accordion-toggle")]')
    num = 1
    for div in divs:
        div_class_names = div.get_attribute('class')
        feature_contents = browser.find(xpath=f'//div[contains(@id, "feature-main-row{num}")]')
        assert feature_contents, 'Sub-contents are not present'

        # Check if the feature section is initially collapsed
        # If it's collapsed, then check if it's opening up and it's sub-sections are displayed or not
        # Else it's open, then check if it's collapsing successfully
        if 'accordion-toggle' in div_class_names and 'collapsed' in div_class_names:
            div.click()
            sleep(3)
            assert feature_contents.is_displayed(), f'Unable to see contents of feature: {div.text}'
        else:
            div.click()
            sleep(3)
            assert feature_contents.is_displayed() is False, f'Unable to collapse feature: {div.text}'
        browser.scroll_down(10)
        num += 1
        sleep(2)

def assert_cards_redirection(browser, cards, redirect_to_urls):
    assert len(cards) > 0, 'Wrong xpath given for cards'
    for card in cards:
        sleep(1)
        card.click()
        sleep(1)
        browser.switch_tab_next(1)
        assert browser.get_current_url() in redirect_to_urls, 'Redirecting to wrong page'
        browser.close_windows()
        sleep(1)

def assert_cta_click_and_modal_show(browser, cta_xpath):
    browser.click(xpath=cta_xpath)
    sleep(2)
    form_modal = browser.find(xpath='//div[contains(@class, "modal-content")]')
    assert form_modal and form_modal.is_displayed(), 'Form modal not visible'
