import zipfile
import gt_api
import os
import json
import sys
import argparse

token = os.environ["GT_TOKEN"]


def clone(map_id, output):
    zf = zipfile.ZipFile(output, "w")
    client = gt_api.Client(token)
    groups = client.get_public_drop_groups(map_id)

    info = client.get_map_info(map_id)
    with zf.open("map_info.json", "w") as f:
        f.write(json.dumps(info).encode("ascii"))

    if not groups:
        drops = client.get_map_drops(map_id)
        with zf.open("drops.json", "w") as f:
            f.write(json.dumps(drops).encode("ascii"))
    else:
        for i, g in enumerate(groups):
            print(f"\r{i/len(groups)*100:.2f}%   ", end="")
            zf.mkdir(str(g["id"]))
            drops = client.get_group_drops(g["id"])
            with zf.open(f"{g['id']}/drops.json", "w") as f:
                f.write(json.dumps(drops).encode("ascii"))
            with zf.open(f"{g['id']}/group_info.json", "w") as f:
                f.write(json.dumps(g).encode("ascii"))


def main():
    parser = argparse.ArgumentParser(
        prog="clone_map.py", description="Saves a geotastic map as a zip archive"
    )
    parser.add_argument("map_id")
    parser.add_argument("output")
    args = parser.parse_args()
    clone(args.map_id, args.output)


if __name__ == "__main__":
    main()
