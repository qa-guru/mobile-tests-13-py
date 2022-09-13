"""
An example of extending Selene with custom commands, specific to mobile context
"""
from selene.core.entity import Element

from mobile_tests_lesson_13.utils.python import monkey


@monkey.patch_method_in(Element)
def tap(self: Element) -> Element:
    return self.click()


@monkey.patch_method_in(Element)
def long_press(self: Element, duration=1.0) -> Element:
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.actions import interaction
    from selenium.webdriver.common.actions.action_builder import ActionBuilder
    from selenium.webdriver.common.actions.pointer_input import PointerInput

    driver = self.config.driver

    actions: ActionChains = ActionChains(driver)

    def fn(element: Element):
        mobile_element = element()

        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, 'touch')
        )
        (
            actions.w3c_actions.pointer_action.move_to(mobile_element)
            .pointer_down()
            .pause(duration)
            .release()
        )
        actions.perform()

    self.wait.command(f'long press with duration={duration}s', fn)

    return self
