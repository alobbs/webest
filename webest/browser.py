import glob
import os
import sys

from selenium import webdriver


PROFILE_DIRS = [
    '~/.mozilla/firefox/*',
    '~/Library/Application Support/Firefox/Profiles/*'
]

default_profile = None


def set_default_profile_path(path):
    global default_profile
    assert os.path.exists(path), "Profile doesn't exist"
    assert os.path.isdir(path), "Profile dir isn't a dir"
    assert os.path.exists(os.path.join(path, 'prefs.js')), "Not a profile dir"
    default_profile = path


def get_default_profile_path(with_name=None):
    # Read all potential directories
    entries = [glob.glob(d) for d in PROFILE_DIRS]

    # Keep the profile dirs only
    dirs = [f for f in entries if os.path.exists(os.path.join(f, 'prefs.js'))]
    assert dirs, "No profile found"

    if with_name:
        dirs = [f for f in entries if with_name in f]
        assert dirs, "No profile found with string %s" % with_name

    # Use the newest
    path = sorted(dirs, key=os.path.getmtime)[0]
    set_default_profile_path(path)


def new(profile_path=None, is_mobile=False,
        load_images=True, win_size=(1280, 800)):
    if not profile_path:
        profile_path = get_default_profile_path()

    profile = webdriver.FirefoxProfile(profile_path)

    if not load_images:
        profile.set_preference('permissions.default.image', 2)

    if is_mobile:
        AGENT = "Mozilla/5.0 (Android 5.1; Tablet; rv:40.0) Gecko/40.0 Firefox/40.0"
        profile.set_preference("general.useragent.override", AGENT)

    browser = webdriver.Firefox(profile)
    browser.set_window_size(*win_size)
    return browser
