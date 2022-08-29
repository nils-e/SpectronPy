from selenium.webdriver.remote.webelement import WebElement


def wrap_element(el: WebElement) -> WebElement:
    return SpectronElement(el)


class SpectronElement(WebElement):
    def __init__(self, el):
        super().__init__(el.parent, el.id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        # nothing to do during exit
        pass
