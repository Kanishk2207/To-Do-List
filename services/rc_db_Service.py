from os import environ as env


class RCDBService(object):

    def __init__(self, session):
        self.session = session
        self.env = env
