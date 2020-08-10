# import time
# from simplebrowser import SimpleBrowser
# import logging
# import pytest
# from common.utils import resize_browser

# @pytest.fixture(scope='function')
# def browser(module_browser, base_url, request):
#     resize_browser(browser=module_browser, resolution=request.param)
#     module_browser.get(base_url + '/alternative/expensify')
#     return module_browser

# @pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
# def test_sitemap_url(browser):
#     current_url = browser.get_current_url()
#     browser.get('https://ww2.fylehq.com/sitemap.xml')
#     links = browser.find_many(xpath='//*[contains(@class, "line")]//*[contains(text(),"https")]')
#     for span in links:
#         time.sleep(2)
#         print(span)
#         assert span == current_url, 'Not in sitemap'
