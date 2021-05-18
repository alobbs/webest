import os
import time
import contextlib

import selenium.common
from selenium import webdriver


@contextlib.contextmanager
def new_auto(*args, **kwargs):
    b = new(*args, **kwargs)
    yield b
    b.quit()


def new(url=None, size=None):
    PATH_CHROMIUM = "/Applications/Chromium.app/Contents/MacOS/Chromium"
    
    # Prefer Chromium over Chrome
    if os.path.exists(PATH_CHROMIUM):
        options = webdriver.ChromeOptions()
        options.binary_location = "/Applications/Chromium.app/Contents/MacOS/Chromium"
        browser = webdriver.Chrome(chrome_options=options)
    else:
        browser = webdriver.Chrome()

    if size:
        assert type(size) == tuple
        assert len(size) == 2
        browser.set_window_size(*size)

    # # On Linux, the focus of the application is in the address bar
    # # of the browser after it is created. That creates problems while
    # # working with some <input> fields. Moving the focus to the app to
    # # the browser panel solves it.
    # #
    # # 1st Tab moves the focus to search box
    # # 2nd Tab moves it further to the browser content
    # if platform.system() == 'Linux':
    #     import pykeyboard
    #     k = pykeyboard.PyKeyboard()
    #     for n in range(2):
    #         k.tap_key('Tab')
    #         time.sleep(0.5)

    if url:
        browser.get(url)

    return browser


def load(b, url, force=False, retries=3, retry_timeout=60):
    assert b, "No browser"

    if (not force) and (b.current_url == url):
        return

    for _try in range(retries):
        try:
            return b.get(url)
        except selenium.common.exceptions.TimeoutException:
            if _try < retries - 1:
                time.sleep(retry_timeout)
            else:
                raise
