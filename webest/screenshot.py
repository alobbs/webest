from . import browser

import PIL.Image


def save(url, fp, **kwargs):
    crop = kwargs.pop('crop', None)

    with browser.new_auto(url, **kwargs) as b:
        b.get_screenshot_as_file(fp)

    if crop:
        assert(type(crop) == tuple)
        img = PIL.Image.open(fp)
        img_cropped = img.crop(crop)
        img_cropped.save(fp)
