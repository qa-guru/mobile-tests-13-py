# Mobile tests on BrowserStack with Python + Pytest + Selene + Appium + Allure

## Lesson plan

### Demo Sample

1. Clone this repo
2. Do `poetry install`
3. Open project in PyCharm, setup interpreter
4. Sign up on BrowserStack
5. Get your username, access key and sample app id
   (somewhere from your [browserstack dashboard getting started guide;)](https://app-automate.browserstack.com/dashboard/v2/quick-start/get-started#introduction))
6. Copy `browserstack_sample.py` from [github.com/browserstack/python-appium-app-browserstack/blob/w3c/android/browserstack_sample.py](https://github.com/browserstack/python-appium-app-browserstack/blob/w3c/android/browserstack_sample.py]) to project root or created `demo` python package, and set your credentials and app id remembered in previous step;)
7. Run file from PyCharm
8. Check the build status (find it in the BrowserStack dashboard - sidebar)

### Run existing tests against locally installed app

To run available tests from this project, in addition to 1-3 steps from [«Demo Sample»](#demo-sample), do:

4. Download wikipedia app apk from https://github.com/wikimedia/apps-android-wikipedia/releases/tag/latest, and store it inside project root with name `app-alpha-universal-release.apk`.
5. Go through [official guide](https://appium.io/docs/en/drivers/android-uiautomator2/) on complete driver setup for android devices. Setup [only one device](https://appium.io/docs/en/writing-running-appium/running-tests/#running-your-test-app-with-appium-android) – either an android emulator or a real android device (connected to your machine). One more real device checklist – [from Zebrunner](https://github.com/zebrunner/mcloud-agent#android-devices) and consider some other developer options like «Stay awake» from [this official android guide](https://developer.android.com/studio/debug/dev-options#general).
   If you want to set up more than one device at once, you have to decide which device to use for tests, get its id from the result of running `adb devices` command and add a `udid=<YOUR_DEVICE_ID>` to the `config.local.env` file.
6. Run tests either from PyCharm or from unix terminal (on Windows, use Git Bash or [WSL](https://learn.microsoft.com/ru-ru/windows/wsl/install))
   ```bash
   pytest tests/android/patched_style/test_wikipedia.py --alluredir reports/
   ```
   
### Run existing tests against browserstack

In addition to 1-5 steps from [«Demo Sample»](#demo-sample), do:

6. Copy `config.personal.env.example` to `config.personal.env` inside the project root
7. Inside `config.personal.env`, set `browserstack.userName` and `browserstack.accessKey` to your values, got on step 5.
8. Run tests from unix terminal (on Windows, use Git Bash or [WSL](https://learn.microsoft.com/ru-ru/windows/wsl/install))
   ```bash
   env -S 'context=personal' pytest tests/android/patched_style/test_wikipedia.py --alluredir reports/
   ```

#### More commandline Tips&Tricks

Notice that, when running from terminal, you can «overwrite» the existing env file, by providing all needed options also by calling a `env` command (available in unix terminals like Git Bash or [WSL](https://learn.microsoft.com/ru-ru/windows/wsl/install)) 

```bash
env -S "app='bs://c700ce60cf13ae8ed97705a55b8e022f13c5827c' appName='org.wikipedia.alpha' remote_url='http://hub.browserstack.com/wd/hub' browserstack.userName='harrypotter_qiHHSb' browserstack.accessKey='fSnAmPdKHW2xsDkV95Zs'" pytest tests/android/patched_style/test_wikipedia.py --alluredir reports/
```

Or you can store all needed options values in a different `config.*.env` file, where * is one of values defined (you can extend them, of course) in config.py at the following lines:

```python
from typing import Literal

EnvContext = Literal['personal', 'test', 'stage', 'prod']
```

Hence, instead of using config.personal.env, you can create, for example the `config.stage.env` file, store there all needed options, and then run tests by something like:

```bash
env -S "context=stage" pytest tests/android/patched_style/test_wikipedia.py --alluredir reports/
```

You also can run tests and execute allure reports in «one shot» by something like:

```bash
env -S "context=stage" pytest tests/android/patched_style/test_wikipedia.py --alluredir reports/; allure serve /reports
```

### FAQ

#### How to upload your own version of application to Browserstack?

Run the following cURL (available from unix terminal, like Git Bash on windows) request (by providing your userName and accessKey in the `-u "<userName>:<accessKey>"` section) to upload an Android app:

```bash
curl -u "alexandersantalov_bsAqLc:N8yqKqzaEWS5DX9ibcJF"  -X POST "https://api-cloud.browserstack.com/app-automate/upload"  -F "file=@/path/to/app/file/application-debug.apk"
```

You should get the following response:

```bash
{
   "app_url":"bs://f7c874f21852ba57957a3fdc33f47514288c4ba4"
}
```

Now you can use the `app_url` value (like `"bs://f7c874f21852ba57957a3fdc33f47514288c4ba4"` from above) to set the corresponding `app` capability in your options to driver (e.g. by setting corresponding env variable in your dotenv files)

See [Official Documentation](https://www.browserstack.com/docs/app-automate/appium/upload-app-from-filesystem) to know more.

#### How to properly pass desired capabilites in Appium Inspector at Windows?

Here is an example of desired capabilities for Windows:

```bash
{
  "automationName": "UIAutomator2",
  "platformName": "Android",
  "app": "F:\\app\\wiki.apk",
  "appWaitActivity": "org.wikipedia.*"
}
```

Notice that there is no `appium:` prefix for some capabilities, that it's Ok to set on Mac OS.

#### How to stream the connected real device screen at your desktop?

Use Scrcpy app ;). See [Documentation](https://github.com/Genymobile/scrcpy) | 
[Downloads](https://github.com/Genymobile/scrcpy/releases/)

#### How to run the english version of a mobile application on your device?

To use, for example, the Wikipedia application on your device with the English interface, change the interface of your device to English.

#### How to set up tests to run on iOS devices?

Get familiar with [official appium guide on initial driver configuration](https://appium.io/docs/en/drivers/ios-xcuitest/). 

To set up real device instead of io emulator check [this dedicated appium guide](https://github.com/appium/appium-xcuitest-driver/blob/master/docs/real-device-config.md)

Consider using [this guide from Zebrunner on how configure iOS devices](https://github.com/zebrunner/mcloud-agent#ios-devices)
