from typing import Union, Tuple

from appium.webdriver.common.appiumby import AppiumBy
from selene import Browser
from selene.core.entity import Element, Collection
from selenium.webdriver.common.by import By
import re

import config
from mobile_tests_lesson_13.utils.python import monkey


def is_word_with_dashes_underscores_or_numbers(selector):
    return re.match(r'^[a-zA-Z_\d\-]+$', selector)


def are_words_with_dashes_underscores_or_numbers_separated_by_space(selector):
    return re.match(r'^[a-zA-Z_\d\- ]+$', selector)


def _by(selector: str | Tuple[str, str]):
    # --- Handle raw locators in tuples ---
    if isinstance(selector, tuple):
        return selector

    # --- Handle XPath ---
    if (
        selector.startswith('/')
        or selector.startswith('./')
        or selector.startswith('..')
        or selector.startswith('(')
        or selector.startswith('*/')
    ):
        return By.XPATH, selector

    # --- Handle custom conventions ---
    if selector.startswith('#') and is_word_with_dashes_underscores_or_numbers(
        selector[1:]
    ):
        appName = config.settings.appName
        return AppiumBy.ID, f'{appName}:id/{selector[1:]}' if appName else selector[1:]

    if selector.startswith('«') and selector.endswith('»'):
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{selector[1:-1]}")',
        )

    if are_words_with_dashes_underscores_or_numbers_separated_by_space(selector):
        return AppiumBy.ACCESSIBILITY_ID, selector

    raise Exception(f'Unsupported selector: {selector}')


original_browser_element = Browser.element


@monkey.patch_method_in(Browser)
def element(self, selector: Union[str, tuple]) -> Element:
    return original_browser_element(self, _by(selector))


original_browser_all = Browser.all


@monkey.patch_method_in(Browser)
def all(self, selector: Union[str, tuple]) -> Collection:
    return original_browser_all(self, _by(selector))


original_element_element = Element.element


@monkey.patch_method_in(Element)
def element(self, selector: Union[str, tuple]) -> Element:
    return original_element_element(self, _by(selector))


original_element_all = Element.all


@monkey.patch_method_in(Element)
def all(self, selector: Union[str, tuple]) -> Collection:
    return original_element_all(self, _by(selector))
