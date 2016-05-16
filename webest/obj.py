import retrying
import selenium
import selenium.webdriver.support.ui as ui

from . import exceptions as ex


@retrying.retry(wait_fixed=1000, retry_on_exception=ex.is_retry_exception)
def get(b, selector, not_found=None):
    try:
        obj = b.find_element_by_css_selector(selector)
    except selenium.common.exceptions.NoSuchElementException:
        return not_found
    return obj


@retrying.retry(wait_fixed=1000, retry_on_exception=ex.is_retry_exception)
def get_objs(b, selector, not_found=None):
    try:
        objs = b.find_elements_by_css_selector(selector)
    except selenium.common.exceptions.NoSuchElementException:
        return not_found
    return objs


@retrying.retry(wait_fixed=1000, retry_on_exception=ex.is_retry_exception)
def is_visible(b, selector):
    try:
        obj = b.find_element_by_css_selector(selector)
    except selenium.common.exceptions.NoSuchElementException:
        return False
    return obj.is_displayed()


@retrying.retry(wait_fixed=1000, retry_on_exception=ex.is_retry_exception)
def is_enabled(b, selector):
    try:
        obj = b.find_element_by_css_selector(selector)
    except selenium.common.exceptions.NoSuchElementException:
        return False
    return obj.is_enabled()


def get_text(b, selector, not_found=None):
    obj = get(b, selector)
    if obj:
        return obj.text
    return not_found


def obj_attr(b, selector, attr, not_found=None):
    obj = get(b, selector)
    if obj:
        re = obj.get_attribute(attr)
        if re is None:
            return not_found
        return re
    return not_found


def wait_for_obj(b, selector, timeout=30):
    wait = ui.WebDriverWait(b, timeout)
    wait.until(lambda driver, s=selector: get(b, s))
    return get(b, selector)


def wait_for_any_obj(b, selectors, timeout=30):
    def check_func(b):
        return any([get(b, s) for s in selectors])

    wait = ui.WebDriverWait(b, timeout)
    wait.until(check_func)

    for s in selectors:
        obj = get(b, s)
        if obj:
            return obj


def wait_while_obj(b, selector, timeout=30):
    wait = ui.WebDriverWait(b, timeout)
    wait.until(lambda driver, s=selector: not get(b, s))
    return get(b, selector)


def wait_while_visible(b, selector, timeout=30):
    wait = ui.WebDriverWait(b, timeout)
    wait.until(lambda driver, s=selector: not get(b, s))
    return get(b, selector)


def wait_while_hiden(b, selector, timeout=30):
    wait = ui.WebDriverWait(b, timeout)
    wait.until(lambda driver, s=selector: get(b, s))
    return get(b, selector)
