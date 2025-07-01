import gt_api
import os
import time
import requests

TOKEN = os.environ["GT_TOKEN"]
guess_data = None



lobby = gt_api.Lobby.create(TOKEN)

@lobby.event_handler("*")
def handle_any(lobby, type, message):
    print(type, message)


@lobby.event_handler("newRoundData")
def handle_new_round_data(lobby, type, message):
    global guess_data
    guess_data = {
        "latLng": {
            "lat": message["partialGameLoop"]["activeTargetDrop"]["lat"],
            "lng": message["partialGameLoop"]["activeTargetDrop"]["lng"],
        },
        "country": "",
        "round": message["partialGameLoop"]["currentRound"],
        "ts": int(time.time() * 1000),
    }

    lobby.send_message("submitGuess", data=guess_data)
    print("SUBMITTED")


@lobby.event_handler("timeUpdate")
def handle_time_update(lobby, type, message):
    if message["time"] != 180:
        return
    lobby.lobby_api_request(
        "https://multiplayer02.geotastic.net/finishGuess",
        "POST",
        json={"data": guess_data, "type": "position"},
    )

    print("FINISHED")


@lobby.event_handler("roundResults")
def handle_round_results(lobby, type, message):
    time.sleep(2)  # s u p e r scuffed
    lobby.send_message("nextRound")


@lobby.event_handler("totalResults")
def handle_total_results(lobby, type, message):
    time.sleep(5)
    lobby.send_message("backToLobby")
    new_game()


lobby.run()


def new_game():
    print("Press ENTER to start game")
    input()
    print("nope")
    lobby.send_message("startGame")


new_game()
