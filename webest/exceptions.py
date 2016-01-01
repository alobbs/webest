import selenium


def is_retry_exception(exception):
    return isinstance(
        exception,
        selenium.common.exceptions.UnexpectedAlertPresentException)
