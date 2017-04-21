from . import obj
from selenium.webdriver.common.keys import Keys

def remove_children(b, selector):
    js = """document.querySelector('%s').innerHTML = '';""" % (selector)
    b.execute_script(js)

def focus(b, selector):
    js = """document.querySelector('%s').focus();""" % (selector)
    b.execute_script(js)
