from selene import have, be
from selene.support.shared import browser
from allure import step as title

from mobile_tests_lesson_13.model import app


def test_search():
    app.given_opened()

    with title('Search for content'):
        browser.element('Search Wikipedia').tap()
        browser.element('#search_src_text').type('BrowserStack')

    with title('Content should be found'):
        browser.all('#page_list_item_title').should(have.size_greater_than(0))
        browser.element('«Software company based in India»').should(be.visible)


def test_search_is_efficient_enough_to_find_selene_as_python_package():
    app.given_opened()

    with title('Search for content'):
        browser.element('Search Wikipedia').tap()
        browser.element('#search_src_text').type('Selene')

    with title('Content should be found'):
        browser.all('#page_list_item_title').first.should(
            have.text('User-oriented Web UI browser tests in Python')
        )
