from . import generic
from .client import Client


@Client._register_endpoint
def get_all_user_challenges(auth_token=None):
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/getAllUserChallenges.php",
            "GET",
            auth_token,
        )
    )


@Client._register_endpoint
def get_challenge_drops(challenge_id, auth_token=None):
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/getChallengeDrops.php",
            "GET",
            auth_token,
            params={"id": challenge_id},
        )
    )


@Client._register_endpoint
def get_challenge(uid, auth_token=None):
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/getChallenge2.php",
            "GET",
            auth_token,
            params={"uid": uid},
        )
    )


@Client._register_endpoint
def get_challenge_results(challenge_id, auth_token=None):
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/getChallengeResults.php",
            "GET",
            auth_token,
            params={"id": challenge_id},
        )
    )


@Client._register_endpoint
def get_own_challenges(auth_token=None):
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/getOwnChallenges.php",
            "GET",
            auth_token,
        )
    )


@Client._register_endpoint
def create_draft_challenge(challenge_name, challenge_type="custom", auth_token=None):
    data = generic.encode_encdata({"name": challenge_name, "mapType": challenge_type})
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/createDraftChallenge.php",
            "POST",
            auth_token,
            json={"enc": data},
        )
    )


@Client._register_endpoint
def update_challenge_pick(
    challenge_id,
    total_score,
    round_no,
    country_score,
    score,
    lat,
    lon,
    distance,
    time,
    country,
    finished=False,
    auth_token=None,
):
    print(
        {
            "id": challenge_id,
            "score": total_score,
            "round": round_no,
            "finished": finished,
            "result": {
                "round": round_no,
                "countryScore": country_score,
                "score": score,
                "distance": distance,
                "time": time,
                "lat": lat,
                "lng": lon,
                "country": country,
                "state": "",
            },
        }
    )

    data = generic.encode_encdata(
        {
            "id": challenge_id,
            "score": total_score,
            "round": round_no,
            "finished": finished,
            "result": {
                "round": round_no,
                "countryScore": country_score,
                "score": score,
                "distance": distance,
                "time": time,
                "lat": lat,
                "lng": lon,
                "country": country,
                "state": "",
            },
        }
    )
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/updateChallengePick.php",
            "POST",
            auth_token,
            json={"enc": data},
        )
    )


@Client._register_endpoint
def update_last_round_seen(challenge_id, round_no, auth_token=None):
    data = generic.encode_encdata({"id": challenge_id, "round": round_no})
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/updateLastRoundSeen.php",
            "POST",
            auth_token,
            json={"enc": data},
        )
    )


@Client._register_endpoint
def finish_challenge(challenge_id, auth_token=None):
    data = generic.encode_encdata({"id": challenge_id})
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/finishChallenge.php",
            "POST",
            auth_token,
            json={"enc": data},
        )
    )


@Client._register_endpoint
def publish_challenge(
    challenge_id, status="published", scheduled_date="", auth_token=None
):
    data = generic.encode_encdata(
        {"challengeId": challenge_id, "status": status, "scheduledDate": scheduled_date}
    )
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/publishChallenge.php",
            "POST",
            auth_token,
            json={"enc": data},
        )
    )


@Client._register_endpoint
def update_challenge(
    challenge_id, name, description, visibility, image="", auth_token=None
):
    data = generic.encode_encdata(
        {
            "id": challenge_id,
            "name": name,
            "description": description,
            "visibility": visibility,
            "image": image,
        }
    )
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/updateChallenge2.php",
            "POST",
            auth_token,
            json={"enc": data},
        )
    )


@Client._register_endpoint
def start_challenge(challenge_uid, auth_token=None):
    data = generic.encode_encdata(
        {
            "uid": challenge_uid,
        }
    )
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/challenge/startChallenge.php",
            "POST",
            auth_token,
            json={"enc": data},
        )
    )
