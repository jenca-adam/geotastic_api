import requests, hashlib, os, base64, json

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

from .errors import GeotasticAPIError

PASSWORD = b"4317969d37f68d4f54eae689d8088eba"  # static


def evp_bytes_to_key(salt, password=PASSWORD, key_len=32, iv_len=16):
    salt = bytes.fromhex(salt)
    d = b""
    while len(d) < key_len + iv_len:
        d_i = (
            hashlib.md5(d[-16:] + password + salt).digest()
            if d
            else hashlib.md5(password + salt).digest()
        )
        d += d_i

    return d[:key_len], d[key_len : key_len + iv_len]


def decode_encdata(plain):
    encdata = json.loads(plain)
    ct = base64.b64decode(encdata["ct"])
    salt = encdata["s"]
    key, iv = evp_bytes_to_key(salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return json.loads(unpad(cipher.decrypt(ct), AES.block_size))


def encode_encdata(data):
    plain = json.dumps(data).encode("utf-8")
    salt = os.urandom(8).hex()
    key, iv = evp_bytes_to_key(salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = base64.b64encode(cipher.encrypt(pad(plain, AES.block_size))).decode("ascii")
    return json.dumps({"ct": ct, "iv": iv.hex(), "s": salt})


def process_response(response):
    if response.ok:
        json_response = response.json()
        if json_response["status"] == "success":
            if json_response.get("enc"):
                return decode_encdata(json_response["encData"])
            return json_response.get("data")
        else:
            raise GeotasticAPIError(json_response["message"])
    else:
        return response
        raise GeotasticAPIError(f"{response.status_code} {response.reason}")


def geotastic_api_request(url, method, auth_token=None, *args, **kwargs):
    # unethical :(

    headers = {"Referer": "https://geotastic.net/", "Origin": "https://geotastic.net"}
    if auth_token:
        headers["X-Auth-Token"] = auth_token

    return requests.request(
        method,
        url,
        headers=headers,
        *args,
        **kwargs,
    )
