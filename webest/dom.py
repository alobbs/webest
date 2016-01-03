def remove_children(b, selector):
    js = """document.querySelector('%s').innerHTML = '';""" % (selector)
    b.execute_script(js)
