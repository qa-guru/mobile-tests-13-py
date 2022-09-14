from appium.webdriver.common.appiumby import AppiumBy
from selene import have
from selene.support.shared import browser
from allure import step

from mobile_tests_lesson_13.model import app


def test_search():
    app.given_opened()

    with step('Search for content'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/search_src_text')).type(
            'BrowserStack'
        )

    with step('Content should be found'):
        browser.all(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')
        ).should(have.size_greater_than(0))
