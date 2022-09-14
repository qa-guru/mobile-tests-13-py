from selene import be
from selene.support.shared import browser


def given_opened():
    if browser.element('#fragment_onboarding_skip_button').matching(be.visible):
        browser.element('#fragment_onboarding_skip_button').tap()
