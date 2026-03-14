from . import generic
from .client import Client
import math


@Client._register_endpoint
def get_app_config(auth_token=None):
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/config/getAppConfig.php",
            "GET",
            auth_token,
        )
    )


@Client._register_endpoint
def get_community_map_markers(auth_token=None):
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/communityMap/getMarkers.php",
            "GET",
            auth_token,
        )
    )


@Client._register_endpoint
def request_api_key(auth_token=None):
    data = generic.encode_encdata({})
    return generic.process_response(
        generic.geotastic_api_request(
            "https://backend03.geotastic.net/v1/config/requestApiKey.php",
            "POST",
            auth_token,
            json={"enc": data},
        )
    )


"""
 zNe = (e, s, t) => e * (1 - t) + s * t;
static calculateFactor(s, t) {
                  return - Math.log(0.5 / s) / t
                }
static calculateScore(s, t, n) {
                  if (s <= n.fullScoreRadius / 1000) return t;
                  if (s > n.maxScoreDistance) return 0;
                  const r = t - n.fullScoreFalloff * t,
                  a = n.fullScoreRadius / 1000,
                  o = Vc.calculateFactor(t, n.maxScoreDistance) * 1, 
                  l = r * Math.pow(Math.E, - o * (s - a)),
                  u = (s - a) * (r / ( - n.maxScoreDistance + a)) + r,
                  d = zNe(l, u, n.linearization);
                  return Math.max(Math.min(t, Math.floor(d)), 0)
                }"""


def calculate_distance_score(
    distance,
    max_score,
    full_score_radius_m,
    max_score_distance_km,
    full_score_falloff,
    linearization,
):
    radius_km = (
        full_score_radius_m / 1000.0
    )  # TODO: check if the full score radius is actually in metres or edu is just bullshitting me.
    # it would make sense though.
    if distance <= radius_km:
        return max_score
    if distance > max_score_distance_km:
        return 0
    max_score_after_falloff = max_score - full_score_falloff * max_score
    factor = (
        -math.log(0.5 / max_score) / max_score_distance_km
    )  # no idea what this is doing.
    l = max_score_after_falloff * math.exp(
        -factor * (distance - radius_km)
    )  # l? idgaf anymore
    u = (distance - radius_km) * (
        max_score_after_falloff / (-max_score_distance_km + radius_km)
    ) + max_score_after_falloff
    d = l * (1 - linearization) + u * linearization
    return max(min(max_score, math.floor(d)), 0)
