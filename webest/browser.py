import functools
import glob
import os

from selenium import webdriver

PROFILE_DIRS = [
    '~/.mozilla/firefox',
    '~/Library/Application Support/Firefox/Profiles',
]

PROFILE_CONF_FILE = "~/.config/webest/firefox_profile"

MOBILE_AGENT = (
    "Mozilla/5.0 (Android 5.1; Tablet; rv:40.0) Gecko/40.0 Firefox/40.0"
)

default_profile = None


def set_default_profile_path(path):
    global default_profile
    assert os.path.exists(path), "Profile doesn't exist"
    assert os.path.isdir(path), "Profile dir isn't a dir"
    assert os.path.exists(os.path.join(path, 'prefs.js')), "Not a profile dir"
    default_profile = path


def get_default_profile_path(check_config_file=True, with_name=None):
    # Has it been set already?
    if default_profile:
        return default_profile

    # Configuration file
    if check_config_file:
        conf_file = os.path.expanduser(PROFILE_CONF_FILE)
        if os.path.exists(conf_file):
            with open(conf_file, 'r') as cf:
                path = cf.readline().strip()
                set_default_profile_path(path)
                return path

    # Read all potential directories
    globs = [os.path.expanduser(d)+'/*' for d in PROFILE_DIRS]
    entries = functools.reduce(lambda x, y: x+y, [glob.glob(d) for d in globs])

    # Keep the profile dirs only
    dirs = [f for f in entries if os.path.exists(os.path.join(f, 'prefs.js'))]
    assert dirs, "No profile found"

    if with_name:
        dirs = [f for f in entries if with_name in f]
        assert dirs, "No profile found with string %s" % with_name

    # Use the newest
    path = sorted(dirs, key=os.path.getmtime)[0]

    # Set it as default
    set_default_profile_path(path)
    return path


def new(url=None, profile_path=None, is_mobile=False,
        load_images=True, size=(1280, 800)):
    # Get path to profile
    if not profile_path:
        profile_path = get_default_profile_path()

    assert os.path.isdir(profile_path), "Profile not found"

    # Tweak profile if needed
    profile = webdriver.FirefoxProfile(profile_path)
    if not load_images:
        profile.set_preference('permissions.default.image', 2)

    if is_mobile:
        profile.set_preference("general.useragent.override", MOBILE_AGENT)

    # Instance new browser window
    browser = webdriver.Firefox(profile)

    if size:
        browser.set_window_size(*size)

    if url:
        browser.get(url)

    return browser
