from .errors import GeotasticAPIError
from .generic import decode_encdata
import requests

FINGERPRINT = "122a458e7f0403b8a5bbc6253a3ab294"  # doesn't really matter but something needs to be there


def login(mail=None, password=None, token=None):
    creds = {}
    if mail:
        creds["mail"] = mail
    if password:
        creds["password"] = password
    if token:
        creds["token"] = token
    print(creds)
    response = requests.post(
        "https://api.geotastic.net/v1/user/login.php",
        headers={
            "Origin": "https://geotastic.net",
            "Referer": "https://geotastic.net/",
        },
        json={"credentials": {"fingerprint": FINGERPRINT, **creds}},
    )
    if response.ok:
        json_response = response.json()
        if json_response["status"] == "success":
            return decode_encdata(json_response["encData"])
        raise GeotasticAPIError(json_response["message"])
    raise GeotasticAPIError(f"{response.status} {response.reason}")
