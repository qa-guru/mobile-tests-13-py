import pydantic
from appium.options.android import UiAutomator2Options
from typing import Literal, Optional

from mobile_tests_lesson_13 import utils

EnvContext = Literal['personal', 'local', 'test', 'stage', 'prod']


class Settings(pydantic.BaseSettings):
    context: EnvContext = 'local'

    # --- Appium Capabilities ---
    platformName: str = None
    platformVersion: str = None
    deviceName: str = None
    app: Optional[str] = None
    appName: Optional[str] = None
    appWaitActivity: Optional[str] = None
    newCommandTimeout: Optional[int] = 60

    # --- > BrowserStack Capabilities ---
    projectName: Optional[str] = None
    buildName: Optional[str] = None
    sessionName: Optional[str] = None
    # --- > > BrowserStack credentials---
    userName: Optional[str] = None
    accessKey: Optional[str] = None
    udid: Optional[str] = None

    # --- Remote Driver ---
    remote_url: str = 'http://127.0.0.1:4723/wd/hub'  # it's a default appium server url

    # --- Selene ---
    timeout: float = 6.0

    @property
    def run_on_browserstack(self):
        return 'hub.browserstack.com' in self.remote_url

    @property
    def driver_options(self):
        options = UiAutomator2Options()
        if self.deviceName:
            options.device_name = self.deviceName
        if self.platformName:
            options.platform_name = self.platformName
        options.app = (
            utils.file.abs_path_from_project(self.app)
            if self.app.startswith('./') or self.app.startswith('../')
            else self.app
        )
        options.new_command_timeout = self.newCommandTimeout
        if self.udid:
            options.udid = self.udid
        if self.appWaitActivity:
            options.app_wait_activity = self.appWaitActivity
        if self.run_on_browserstack:
            options.load_capabilities(
                {
                    'platformVersion': self.platformVersion,
                    'bstack:options': {
                        'projectName': self.projectName,
                        'buildName': self.buildName,
                        'sessionName': self.sessionName,
                        'userName': self.userName,
                        'accessKey': self.accessKey,
                    },
                }
            )

        return options

    @classmethod
    def in_context(cls, env: Optional[EnvContext] = None) -> 'Settings':
        """
        factory method to init Settings with values from corresponding .env file
        """
        asked_or_current = env or cls().context
        return cls(
            _env_file=utils.file.abs_path_from_project(f'config.{asked_or_current}.env')
        )


settings = Settings.in_context()
