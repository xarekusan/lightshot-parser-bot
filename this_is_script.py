import httplib2
import random
import string
from os import path
from bs4 import BeautifulSoup


class Main:
    def __init__(self, url_img):
        self.h = httplib2.Http('.cache')
        self.response, self.content = self.h.request(url_img)
        self.filename = path.basename(url_img)
        open(self.filename, 'wb').write(self.content)

    def open(self):
        return self.filename


class Generator:
    def __init__(self, size=5, chars=string.ascii_lowercase + string.digits):
        self.name = ''.join(random.SystemRandom().choice(chars) for _ in range(size))
        self.url = ''.join("https://prnt.sc/10" + self.name)

    def generator(self):
        return self.name, self.url


class Request:
    def __init__(self, url):
        self.h = httplib2.Http('.cache')
        self.response, self.content = self.h.request(url)
        self.soup = BeautifulSoup(self.content)
        self.image = self.soup.findAll('img')[0]
        self.url_img = self.image['src']

    def request(self):
        return self.url_img


def start_script():
    name, url_name = Generator().generator()
    url_img = Request(url_name).request()
    try:
        Main(url_img)
    except httplib2.error.RelativeURIError:
        return start_script()
    return Main(url_img).open()
