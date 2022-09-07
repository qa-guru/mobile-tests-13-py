import allure_commons
import pytest
from selene.support.shared import browser
from selene import support
from appium import webdriver

import config


@pytest.fixture(scope='function', autouse=True)
def driver_management():
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )
    browser.config.driver = webdriver.Remote(
        config.settings.remote_url, options=config.settings.driver_options
    )
    browser.config.timeout = config.settings.timeout

    yield

    # TODO: implement logging attachments to Allure Report based on:
    # - java examples:
    #   - https://github.com/qa-guru/mobile-tests-13/blob/master/src/test/java/helpers/Attach.java
    #   - https://github.com/qa-guru/mobile-tests-13/blob/master/src/test/java/helpers/Browserstack.java
    # - and official allure docs for python:
    #   - https://docs.qameta.io/allure#_attachments_5

    # session_id = assist.webdriver.get_session_id();

    # attach.screenshot_as("Last screenshot");
    # attach.page_source();

    browser.quit()
    '''
    # was:
    step("Close driver", Selenide::closeWebDriver);
    '''

    # attach.video(session_id);
