from . import generic
from .client import Client


@Client._register_endpoint
def get_all_hunts(auth_token=None, session=None):
    return generic.process_response(
        generic.geotastic_api_request(
            session,
            "https://backend03.geotastic.net/v1/highscoreHunt/getAllHighscoreHunts.php",
            "GET",
            auth_token,
        )
    )


@Client._register_endpoint
def get_highscore_hunt_state(auth_token=None, session=None):
    return generic.process_response(
        generic.geotastic_api_request(
            session,
            "https://backend03.geotastic.net/v1/highscoreHunt/getHighscoreHuntsState.php",
            "GET",
            auth_token,
        )
    )
