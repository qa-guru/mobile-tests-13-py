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

### Demo Simple Framework

TODO: document rest of the demo

Prerequisites:
- to run tests locally – download wikipedia app apk from https://github.com/wikimedia/apps-android-wikipedia/releases/tag/latest

Examples of usage:

to run with config.local.env:

```bash
pytest tests/android/patched_style/test_wikipedia.py --alluredir reports/
```

to run with config.personal.env (create it first):
```bash
env -S 'context=personal' pytest tests/android/patched_style/test_wikipedia.py --alluredir reports/
```


