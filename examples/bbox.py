import gt_api
import os
import argparse

token = os.environ.get("GT_TOKEN")


def get_bbox(drops):
    minx, miny, maxx, maxy = float("inf"), float("inf"), -float("inf"), -float("inf")
    for drop in drops:
        lon, lat = drop["lng"], drop["lat"]
        minx = min(minx, lon)
        miny = min(miny, lat)
        maxx = max(maxx, lon)
        maxy = max(maxy, lat)
    return [minx, miny, maxx, maxy]


def main():
    parser = argparse.ArgumentParser(
        prog="fix_bbox.py",
        description="Automatically fixes  the bounding boxes for every drop group in a geotastic map",
    )
    parser.add_argument("map_id")
    args = parser.parse_args()
    map_id = args.map_id
    client = gt_api.Client(token)
    map_info = client.get_map_info(map_id)
    if map_info["dropType"] == "single":
        drops = client.get_map_drops(map_id)
        map_bbox = get_bbox(drops)
        client.update_map(map_id, bbox=map_bbox)
    else:
        minx, miny, maxx, maxy = (
            float("inf"),
            float("inf"),
            -float("inf"),
            -float("inf"),
        )
        groups = client.get_public_drop_groups(map_id)
        for i, g in enumerate(groups):
            print(f"\r{i/len(groups)*100:.2f}%   ", end="")
            drops = client.get_group_drops(g["id"])
            group_bbox = gminx, gminy, gmaxx, gmaxy = get_bbox(drops)
            client.update_drop_group(g["id"], bbox=group_bbox)
            minx = min(minx, gminx)
            miny = min(miny, gminy)
            maxx = max(maxx, gmaxx)
            maxy = max(maxy, gmaxy)
        client.update_map(map_id, bbox=[minx, miny, maxx, maxy])


if __name__ == "__main__":
    main()
