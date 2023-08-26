import csv

import httpx
from geo_dist_prep.data import DIST_DATA, NODE_PAIRS
from geo_dist_prep.model.normalize import measure

url = "http://localhost:8080/ors/v2/directions/driving-car"


def road_distance(client, row):
    params = {
        "start": f'{row["lon1"]},{row["lat1"]}',
        "end": f'{row["lon2"]},{row["lat2"]}',
    }
    response = client.get(url, params=params).json()

    return response["features"][0]["properties"]["summary"]["distance"]


def create_training_data():
    fin = open(NODE_PAIRS, "rt")
    reader = csv.DictReader(fin, delimiter="\t")

    fout = open(DIST_DATA, "wt")
    writer = csv.writer(fout, delimiter="\t")
    header = ["lon1", "lat1", "lon2", "lat2", "by_road", "by_air", "angle"]
    writer.writerow(header)

    client = httpx.Client(http2=True)

    errors = total = 0

    for row in reader:
        total += 1
        try:
            road = road_distance(client, row)
        except KeyError:
            errors += 1
            continue
        except httpx.HTTPError:
            errors += 1
            print("HTTP timeout")
            continue

        air, angle = measure(row)

        out = [row["lon1"], row["lat1"], row["lon2"], row["lat2"], road, air, angle]
        writer.writerow(out)

        if total % 1000 == 0:
            print(f"Processed {total} rows ({total-errors} clean)")

    client.close()

    print(f"Errors: {errors}")
    print(f"Total: {total}")


if __name__ == "__main__":
    create_training_data()
