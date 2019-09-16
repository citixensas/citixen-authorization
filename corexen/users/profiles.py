class BaseProfileFinder(object):

    def __init__(self, user,  app, headquarter):
        self.user = user
        self.app = app
        self.headquarter = headquarter

    def get(self):
        raise NotImplementedError('Not implemented')
