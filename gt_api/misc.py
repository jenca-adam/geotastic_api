from . import generic


def get_app_config(auth_token=None):
    return generic.process_response(
        generic.geotastic_api_request(
            "https://api.geotastic.net/v1/config/getAppConfig.php", "GET", auth_token
        )
    )


def get_community_map_markers(auth_token=None):
    return generic.process_response(
        generic.geotastic_api_request(
            "https://api.geotastic.net/v1/communityMap/getMarkers.php",
            "GET",
            auth_token,
        )
    )
