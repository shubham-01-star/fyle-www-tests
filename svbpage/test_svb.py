import time
import logging
import pytest
from common.utils import resize_browser
from common.asserts import assert_customer_logo, assert_customer_testimonial, assert_typography, assert_overflowing
from common.svb_form import assert_required_fields_top, assert_bad_email_top, assert_non_business_email_top, assert_success_form_top, assert_svb_contact_form_required_fields, assert_svb_contact_form_invalid_name, assert_svb_contact_form_invalid_phone, assert_svb_contact_form_invalid_phone_length_min, assert_svb_contact_form_invalid_phone_length_max, assert_svb_contact_form_success

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    time.sleep(0.5)
    module_browser.get(base_url + '/svb')
    return module_browser

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_customer_logo(browser):
    assert_customer_logo(browser)

@pytest.mark.parametrize('browser', [('desktop_1')], indirect=True)
def test_customer_testimonial(browser):
    assert_customer_testimonial(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_page_overflow(browser):
    assert_overflowing(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_typography(browser):
    assert_typography(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_required_fields_top(browser):
    assert_required_fields_top(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email_top(browser):
    assert_bad_email_top(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_non_business_email_top(browser):
    assert_non_business_email_top(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success_form_top(browser):
    assert_success_form_top(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_svb_contact_form_required_fields(browser):
    assert_svb_contact_form_required_fields(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_svb_contact_form_invalid_name(browser):
    assert_svb_contact_form_invalid_name(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_svb_contact_form_invalid_phone(browser):
    assert_svb_contact_form_invalid_phone(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_svb_contact_form_invalid_phone_length_min(browser):
    assert_svb_contact_form_invalid_phone_length_min(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_svb_contact_form_invalid_phone_length_max(browser):
    assert_svb_contact_form_invalid_phone_length_max(browser)

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_svb_contact_form_success(browser):
    assert_svb_contact_form_success(browser)
