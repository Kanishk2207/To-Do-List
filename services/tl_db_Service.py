from os import environ as env


class TLDBService(object):

    def __init__(self, session):
        self.session = session
        self.env = env
