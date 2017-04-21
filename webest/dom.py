from . import obj
from selenium.webdriver.common.keys import Keys

def remove_children(b, selector):
    js = """document.querySelector('%s').innerHTML = '';""" % (selector)
    b.execute_script(js)

def focus(b, selector):
    o = obj.get(b, selector)
    o.send_keys(Keys.Tab)
