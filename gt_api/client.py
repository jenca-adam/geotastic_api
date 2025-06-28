import functools
from . import login


class Client:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    @classmethod
    def _register_endpoint(cls, endpoint, name=None):
        name = name or endpoint.__name__

        @functools.wraps(endpoint)
        def replaced(self, *args, **kwargs):
            return endpoint(*args, **kwargs, auth_token=self.auth_token)

        setattr(cls, name, replaced)
        return endpoint

    @classmethod
    def login(cls, mail, password):
        login_result = login.login(mail=mail, password=password)
        return cls(login_result["token"])

    def __repr__(self):
        return f"<Client (auth_token={self.auth_token!r})>"
