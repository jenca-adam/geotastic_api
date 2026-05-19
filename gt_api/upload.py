from . import generic
from .client import Client


@Client._register_endpoint
def upload_file(
    files, target, with_full_upload_path=False, auth_token=None, session=None
):
    return generic.process_response(
        generic.geotastic_api_request(
            session,
            "https://upload02.edutastic.de/put.php",
            "POST",
            auth_token,
            params={
                "target": target,
                "withFullUploadPath": str(with_full_upload_path).lower(),
            },
            files=files,
        )
    )


@Client._register_endpoint
def upload_remote_image(image_url, target, auth_token=None, session=None):
    return generic.process_response(
        generic.geotastic_api_request(
            session,
            "https://upload02.edutastic.de/putRemoteImage.php",
            "POST",
            auth_token,
            json={"enc": generic.encode_encdata({"url": image_url, "target": target})},
        )
    )
