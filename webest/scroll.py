import retrying

from . import exceptions as ex


@retrying.retry(wait_fixed=1000, retry_on_exception=ex.is_retry_exception)
def go_bottom(b):
    b.execute_script("window.scrollBy(0,100000)")


@retrying.retry(wait_fixed=1000, retry_on_exception=ex.is_retry_exception)
def go_top(b):
    b.execute_script("window.scrollTo(0,0)")
