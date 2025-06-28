import functools
from . import login


class Client:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    def get_user_data(self):
        return login.login(token=self.auth_token)

    @classmethod
    def _register_endpoint(cls, endpoint):

        @functools.wraps(endpoint)
        def replaced(self, *args, **kwargs):
            return endpoint(*args, **kwargs, auth_token=self.auth_token)

        setattr(cls, endpoint.__name__, replaced)
        return endpoint

    @classmethod
    def login(cls, mail, password):
        login_result = login.login(mail=mail, password=password)
        return cls(login_result["token"])

    def __repr__(self):
        return f"<Client (auth_token={self.auth_token!r})>"
