import os
import gt_api
import threading
import random
import time

token = os.environ["GT_TOKEN"]

lobby = gt_api.Lobby.join(token, input("Lobby id:"))
lobby.run()


def spam_emotes():
    items = gt_api.generic.process_response(
        gt_api.generic.geotastic_api_request(
            "https://api.geotastic.net/v1/items/getItems.php", "GET"
        )
    )
    emotes = [it for it in items if it["type"] == "emote"]
    while True:
        emote = random.choice(emotes)
        lobby.send_message("submitChatKey", data=f"{{{{itemUid:{emote['uid']}}}}}")
        time.sleep(0.2)


threading.Thread(target=spam_emotes).start()
