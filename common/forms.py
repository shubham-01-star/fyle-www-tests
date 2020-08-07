import time
import logging

logger = logging.getLogger(__name__)

def submit_content_download_form(browser, email=None, firstname=None, lastname=None, company_size=None, agree=None):
    browser.find(xpath="//form[contains(@id, 'content-download-form')]", scroll=True)
    time.sleep(2)
    if firstname:
        browser.input(xpath="//form[contains(@id, 'content-download-form')]//input[@name='firstname']", keys=firstname)
    if lastname:
        browser.input(xpath="//form[contains(@id, 'content-download-form')]//input[@name='lastname']", keys=lastname)
    if email:
        browser.input(xpath="//form[contains(@id, 'content-download-form')]//input[@name='email']", keys=email)
    if company_size:
        browser.click(xpath="//form[contains(@id, 'content-download-form')]//input[@id='number_of_employees']")
        browser.click(xpath=f"//form[contains(@id, 'content-download-form')]//li[@data-value='{company_size}']")
    if agree:
        browser.click(xpath="//form[contains(@id, 'content-download-form')]//div[contains(@class, 'custom-checkbox')]")
    browser.click(xpath="//form[contains(@id, 'content-download-form')]//button[contains(@id, 'form-button')]")

def submit_download_excel_form(browser, email=None, firstname=None, lastname=None, company_size=None, agree=None):
    browser.click(xpath="//a[@id='download-excel']")
    if firstname:
        browser.input(xpath="//form[contains(@id, 'content-download-form')]//input[@name='firstname']", keys=firstname)
    if lastname:
        browser.input(xpath="//form[contains(@id, 'content-download-form')]//input[@name='lastname']", keys=lastname)
    if email:
        browser.input(xpath="//form[contains(@id, 'content-download-form')]//input[@name='email']", keys=email)
    if company_size:
        browser.click(xpath="//form[contains(@id, 'content-download-form')]//input[@id='number_of_employees']")
        browser.click(xpath=f"//form[contains(@id, 'content-download-form')]//li[@data-value='{company_size}']")
    if agree:
        browser.click(xpath="//form[contains(@id, 'content-download-form')]//div[contains(@class, 'custom-checkbox')]")
    browser.click(xpath="//form[contains(@id, 'content-download-form')]//button[text()='Download']")
    