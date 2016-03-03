import retrying

from . import exceptions as ex


@retrying.retry(wait_fixed=1000, retry_on_exception=ex.is_retry_exception)
def back(b):
    b.execute_script("history.back()")

@retrying.retry(wait_fixed=1000, retry_on_exception=ex.is_retry_exception)
def forward(b):
    b.execute_script("history.forward()")
