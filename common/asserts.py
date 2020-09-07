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

def assert_hero_image(browser):
    hero_image = browser.find(xpath='//section[contains(@class,  "new-hero")]//img')
    assert hero_image.is_displayed() is False, 'Hero image is being shown in mobile'

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

# Commented out the other sections typography because of inconsistencies
def assert_typography(browser):
    sections = browser.find_many(xpath='//section')
    hero_section = sections[0]
    # other_sections = sections[1:]
    assert_hero_section(browser=browser, section=hero_section)
    # for other_section in other_sections:
    #     assert_other_section(browser=browser, section=other_section)

def assert_spacing_between(element1=None, element2=None, value=None):
    padding_below = int(element1.value_of_css_property('padding-bottom').replace('px', ''))
    margin_below = int(element1.value_of_css_property('margin-bottom').replace('px', ''))
    space_below = padding_below + margin_below
    padding_top = int(element2.value_of_css_property('padding-top').replace('px', ''))
    margin_top = int(element2.value_of_css_property('margin-top').replace('px', ''))
    space_top = padding_top + margin_top
    space_between = space_below + space_top
    assert space_between == value, "spacing between is not correct"

def assert_horizontal_spacing_between(element1=None, element2=None, value=None):
    padding_right = int(element1.value_of_css_property('padding-right').replace('px', ''))
    margin_right = int(element1.value_of_css_property('margin-right').replace('px', ''))
    space_right = padding_right + margin_right
    padding_left = int(element2.value_of_css_property('padding-left').replace('px', ''))
    margin_left = int(element2.value_of_css_property('margin-left').replace('px', ''))
    space_left = padding_left + margin_left
    space_between = space_right + space_left
    assert space_between == value, f"Horizontal spacing between elements '{element11}' and '{element2}' is not correct"

def assert_spacing_bottom(element=None, value=None):
    padding_below = int(element.value_of_css_property('padding-bottom').replace('px', ''))
    margin_below = int(element.value_of_css_property('margin-bottom').replace('px', ''))
    space_below = padding_below + margin_below
    assert space_below == value, "spacing below is not correct"

def assert_spacing_top(element=None, value=None):
    padding_top = int(element.value_of_css_property('padding-top').replace('px', ''))
    margin_top = int(element.value_of_css_property('margin-top').replace('px', ''))
    space_top = padding_top + margin_top
    assert space_top == value, "spacing top is not correct"

def assert_spacing_right(element=None, value=None):
    padding_right = int(element.value_of_css_property('padding-right').replace('px', ''))
    margin_right = int(element.value_of_css_property('margin-right').replace('px', ''))
    space_top = padding_right + margin_right
    assert space_top == value, f"spacing right is not correct for '{element.text}'"

def assert_spacing_left(element=None, value=None):
    padding_left = int(element.value_of_css_property('padding-left').replace('px', ''))
    margin_left = int(element.value_of_css_property('margin-left').replace('px', ''))
    space_top = padding_left + margin_left
    assert space_top == value, "spacing left is not correct"

def assert_thank_you_modal(browser, ty_message, demoform=None):
    e = browser.find(xpath="//div[contains(@id, 'contact-us-ty-modal')]")
    assert e and e.is_displayed, "Thank you modal is not displayed"
    if demoform:
        ty_img = browser.find(xpath="//div[contains(@id, 'contact-us-ty-modal')]//div[contains(@class, 'demo-form-thank-you-img')]")
    else:
        ty_img = browser.find(xpath="//div[contains(@id, 'contact-us-ty-modal')]//div[not(contains(@class, 'demo-form-thank-you-img'))]")
    assert ty_img and ty_img.is_displayed(), "Thank image is not correct"
    ty_text = browser.find(xpath="//div[contains(@id, 'contact-us-ty-modal')]//span[contains(@class, 'ty-box')]").text
    assert ty_text == ty_message, "Thank you message is not correct"

def assert_collapsible_feature_comparison_table(browser):
    section = browser.find(xpath='//section[contains(@class, "alternative-fyle-comparison")]', scroll=True)
    assert section, 'Collapsible table not found'
    divs = browser.find_many(xpath='//div[contains(@class, "accordion-toggle")]')
    for i, div in enumerate(divs):
        div_class_names = div.get_attribute('class')
        sub_contents_div_xpath = f'//div[contains(@id, "feature-main-row{i+1}")]'

        # Check if the feature section is initially collapsed
        # If it's collapsed, then check if it's opening up and it's sub-sections are displayed or not
        # Else it's open, then check if it's collapsing successfully
        if 'accordion-toggle' in div_class_names and 'collapsed' in div_class_names:
            browser.click_element(div)
            feature_contents = browser.find(xpath=sub_contents_div_xpath)
            assert feature_contents.is_displayed(), f'Unable to see contents of feature: {div.text}'
        else:
            browser.click_element(div)
            feature_contents = browser.find(xpath=sub_contents_div_xpath)
            assert feature_contents.is_displayed() is False, f'Unable to collapse feature: {div.text}'
        browser.scroll_up_or_down(50)

def assert_cards_redirection(browser, cards_xpath, redirect_to_urls, same_tab=False):
    if same_tab:
        for i, card_elem in enumerate(cards_xpath):
            card = browser.find(card_elem, scroll=True)
            browser.scroll_up_or_down(-100)
            browser.click_element(card)
            assert browser.get_current_url() == redirect_to_urls[i], "Redirecting to wrong page"
            browser.back()
    else:
        cards = browser.find_many(xpath=cards_xpath)
        assert len(cards) > 0, 'Wrong xpath given for cards'
        for card in cards:
            browser.click_element(card)
            browser.switch_tab_next(1)
            assert browser.get_current_url() in redirect_to_urls, 'Redirecting to wrong page'
            browser.close_windows()
            if browser.is_desktop() is False:
                browser.scroll_up_or_down(300)
            sleep(2)

def assert_cta_click_and_modal_show(browser, cta_section_xpath, cta_xpath):
    section = browser.find(xpath=cta_section_xpath, scroll=True)
    assert section and section.is_displayed(), 'Section not found'
    browser.click(xpath=cta_xpath)
    form_modal = browser.find(xpath='//div[contains(@class, "modal-content")]', scroll=True)
    assert form_modal and form_modal.is_displayed(), 'Form modal not visible'

def assert_overflowing(browser):
    assert browser.check_horizontal_overflow(), f'Horizontal Overflow is there in the page {browser.get_current_url()}'

def assert_customer_logo(browser):
    browser.set_local_storage('ipInfo', '{"ip":"157.50.160.253","country":"India"}')
    browser.refresh()
    sleep(3)
    indian_logo = browser.find("//div[contains(@class, 'customer-logo-india')]")
    us_logo = browser.find("//div[contains(@class, 'customer-logo-non-india')]")
    assert indian_logo.is_displayed() and not us_logo.is_displayed(), 'Found an US image in Indian IP'

    browser.set_local_storage('ipInfo', '{"ip":"157.50.160.253","country":"United States"}')
    browser.refresh()
    sleep(3)
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
    carousel_items = browser.find_many("//section[contains(@class, 'customer-testimonial')]//div[contains(@class, 'carousel-item')]")
    carousel_length = len(carousel_items)
    current_active_index = get_active_index(carousel_items)

    browser.find(xpath="//section[contains(@class, 'customer-testimonial')]", scroll=True)
    sleep(1)
    right_arrow = browser.find(xpath="//section[contains(@class, 'customer-testimonial')]//div[contains(@id, 'customer-carousel')]//a[contains(@class, 'right')]")
    browser.find(xpath="//section[contains(@class, 'customer-testimonial')]//div[contains(@id, 'customer-carousel')]//a[contains(@class, 'right')]//span//img")
    browser.click_element(right_arrow)
    active_index = get_active_index(carousel_items)
    assert active_index == ((current_active_index + 1) % carousel_length), 'Right click operation is not working'

    current_active_index = active_index
    left_arrow = browser.find(xpath="//section[contains(@class, 'customer-testimonial')]//div[contains(@id, 'customer-carousel')]//a[contains(@class, 'left')]")
    browser.find(xpath="//section[contains(@class, 'customer-testimonial')]//div[contains(@id, 'customer-carousel')]//a[contains(@class, 'left')]//span//img")
    browser.click_element(left_arrow)
    active_index = get_active_index(carousel_items)
    assert active_index == ((current_active_index + (carousel_length - 1)) % carousel_length), 'Left click operation is not working'

def assert_spacing_between_text_image(browser, section_xpath):
    section = browser.find(xpath=section_xpath, scroll=True)
    assert_spacing_top(section, 80)
    assert_spacing_bottom(section, 80)
    columns = browser.find_many(xpath=f"{section_xpath}//div[contains(@class, 'container')]//div[contains(@class, 'row')]//div[contains(@class, 'col')]")
    for idx, val in enumerate(columns):
        # Iterate on all divs having text as well as image
        # Checing if idx is odd or even, and thus checking spacing for alternate divs
        if idx^1 == idx+1:
            assert_horizontal_spacing_between(element1=columns[idx], element2=columns[idx+1], value=60)
        else:
            continue

def assert_click_scroll_into_view(browser, clickable_elements_xpath):
    clickable_elements = browser.find_many(xpath=clickable_elements_xpath)
    for ele in clickable_elements:
        browser.click_element(ele)
        assert ele.is_displayed(), "Clicking element '{ele.text}' scrolled to wrong section"
