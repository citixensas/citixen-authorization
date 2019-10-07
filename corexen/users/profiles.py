class BaseProfileFinder(object):

    def __init__(self, user, app_id, headquarter_id, exclude_headquarter_validation=False):
        self.user = user
        self.app = app_id
        self.headquarter = headquarter_id
        self.exclude_headquarter_validation = exclude_headquarter_validation

    def get(self):
        raise NotImplementedError('Not implemented')
