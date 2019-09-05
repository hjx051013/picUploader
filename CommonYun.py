from abc import abstractmethod


class CommonYun(object):
    def __init__(self, domain):
        self.domain = domain

    @abstractmethod
    def upload_file(self): pass
