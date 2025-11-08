import gt_api
import os
import json
import tqdm

ITERATIONS = 1
client = gt_api.Client(os.environ.get("GT_TOKEN"))


def get_leaderboard_uids():
    leaderboard = client.get_season_progress_leaderboard(2)
    return {user["uid"] for user in leaderboard["leaderboard"]}


def get_all_games(uid):
    offset = 0
    games = []
    while True:
        chunk = client.get_ranked_matchmaking_games(uid, offset)
        offset += len(chunk)
        filtered = [game for game in chunk if game["matchmakingId"] >= 15]
        if not filtered:
            break
        games.extend(filtered)
    return games


def get_opponent(lobby_id, uid):
    game_details = client.get_game_history_details(lobby_id)
    for result in game_details["results"]:
        if result["userUid"] != uid:
            return result["userUid"]
    return uid  # discard


def expand(uids):
    old_size = len(uids)
    for uid in sorted(uids):
        games = get_all_games(uid)
        print("player", uid, "has", len(games), "ranked season 1 games")
        for game in tqdm.tqdm(games):
            opponent = get_opponent(game["lobbyId"], uid)
            uids.add(opponent)
        print("added", len(uids) - old_size, "players")
    print("Iteration added", len(uids) - old_size, "players")
    return len(uids) - old_size


def main():
    uids = get_leaderboard_uids()
    for i in range(ITERATIONS):
        expand(uids)
    uid_list = list(uids)
    with open("out.json", "w") as f:
        json.dump(uid_list, f)


if __name__ == "__main__":
    main()
