class BaseMixin:

    fixture = None
    params = None
    token = 'abc123'

    def get_fixture(self):
        return self.fixture

    def get_params(self, **kwargs):  # noqa
        return self.params

    def get_token(self):
        return self.token
