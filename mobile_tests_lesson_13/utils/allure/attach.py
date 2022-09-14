import allure
from selene.support.shared import browser

import config
from mobile_tests_lesson_13 import utils


def screenshot(*, name='screenshot'):
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


def screen_xml_dump(*, name=None):
    allure.attach(
        browser.driver.page_source,
        name=name or 'page xml dump',
        attachment_type=allure.attachment_type.XML,
    )


def screen_html_dump(*, name=None):
    allure.attach(
        browser.driver.page_source,
        name=name or 'page html dump',
        attachment_type=allure.attachment_type.HTML,
    )


def video_from_browserstack(session_id, *, name='video recording'):
    video_url = utils.browserstack.get.video_url(session_id=session_id)

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name=name,
        attachment_type=allure.attachment_type.HTML,
    )
