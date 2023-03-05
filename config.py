import pydantic
from appium.options.android import UiAutomator2Options
from typing import Literal, Optional

from mobile_tests_lesson_13 import assist

EnvContext = Literal['personal', 'test', 'stage', 'prod']


class Settings(pydantic.BaseSettings):
    context: EnvContext = 'personal'

    # --- Appium Capabilities ---
    platformName: str = 'android'
    platformVersion: str = '9.0'
    deviceName: str = 'Google Pixel 3'
    app: Optional[str] = None
    appName: Optional[str] = None

    # --- > BrowserStack Capabilities ---
    projectName: Optional[str] = None
    buildName: Optional[str] = None
    sessionName: Optional[str] = None
    # --- > > BrowserStack credentials---
    userName: Optional[str] = pydantic.Field(None, env='browserstack.userName')
    accessKey: Optional[str] = pydantic.Field(None, env='browserstack.accessKey')
    '''
    # will work only on mac os or linux:
    userName: Optional[str] = None
    accessKey: Optional[str] = None
    
    # will work both on mac os with userName as env var name, 
    # and on windows with 'browserstack.userName' var name
    userName: Optional[str] = pydantic.Field(None, env=['browserstack.userName', 'userName'])
    accessKey: Optional[str] = pydantic.Field(None, env=['browserstack.accessKey', 'accessKey'])
    
    # see more in docs: https://docs.pydantic.dev/usage/settings/#environment-variable-names
    '''

    # --- Remote Driver ---
    remote_url: str = 'http://127.0.0.1:4723/wd/hub'  # it's a default appium server url

    # --- Selene ---
    timeout: float = 6.0

    @property
    def driver_options(self):
        options = UiAutomator2Options()
        options.device_name = self.deviceName
        options.platform_name = self.platformName
        options.app = self.app
        if 'hub.browserstack.com' in self.remote_url:
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
            _env_file=assist.file.abs_path_from_project(
                f'config.{asked_or_current}.env'
            )
        )


settings = Settings.in_context()
