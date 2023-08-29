from geo_dist_prep.data import GEONAMES_DB
from geo_dist_prep.data.docker.regions import group_countries_by_region
from geo_dist_prep.data.docker.run import running_docker_container
from geo_dist_prep.schemas.job import Base, GeoNameEnrichJob, GeoNamePairJob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "http://localhost:8080/ors/v2/directions/driving-car"


def road_distance(client, row):
    params = {
        "start": f'{row["lon1"]},{row["lat1"]}',
        "end": f'{row["lon2"]},{row["lat2"]}',
    }
    response = client.get(url, params=params).json()

    return response["features"][0]["properties"]["summary"]["distance"]


# def create_training_data():
#     fin = open(NODE_PAIRS, "rt")
#     reader = csv.DictReader(fin, delimiter="\t")

#     fout = open(DIST_DATA, "wt")
#     writer = csv.writer(fout, delimiter="\t")
#     header = ["lon1", "lat1", "lon2", "lat2", "by_road", "by_air", "angle"]
#     writer.writerow(header)

#     client = httpx.Client(http2=True)

#     errors = total = 0

#     for row in reader:
#         total += 1
#         try:
#             road = road_distance(client, row)
#         except KeyError:
#             errors += 1
#             continue
#         except httpx.HTTPError:
#             errors += 1
#             print("HTTP timeout")
#             continue

#         air, angle = measure(row)

#         out = [row["lon1"], row["lat1"], row["lon2"], row["lat2"], road, air, angle]
#         writer.writerow(out)

#         if total % 1000 == 0:
#             print(f"Processed {total} rows ({total-errors} clean)")

#     client.close()

#     print(f"Errors: {errors}")
#     print(f"Total: {total}")


def get_pending_countries():
    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    pair_jobs = session.query(GeoNamePairJob).filter(GeoNamePairJob.success).all()
    completed_enrich_jobs = (
        session.query(GeoNameEnrichJob).filter(GeoNameEnrichJob.success).all()
    )
    enriched_pair_job_ids = [job.pair_job_id for job in completed_enrich_jobs]
    pending_countries = [
        job.country_code for job in pair_jobs if job.id not in enriched_pair_job_ids
    ]

    session.close()

    return pending_countries


def enrich(country_code):
    raise NotImplementedError("TODO")


def main():
    pending_countries = get_pending_countries()
    print("enrich:", len(pending_countries), "left to go")

    groups = group_countries_by_region(pending_countries)

    for region, countries in groups.items():
        with running_docker_container(region):
            for country_code in countries:
                enrich(country_code)


if __name__ == "__main__":
    main()
    raise Exception("stop")
