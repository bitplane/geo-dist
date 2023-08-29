import json
from concurrent.futures import ProcessPoolExecutor

import httpx
from geo_dist_prep.data import GEONAMES_DB
from geo_dist_prep.data.docker.regions import group_countries_by_region
from geo_dist_prep.data.docker.run import running_docker_container
from geo_dist_prep.schemas.geoname import GeoName
from geo_dist_prep.schemas.geoname_pair import GeoNamePair
from geo_dist_prep.schemas.job import Base, GeoNameEnrichJob, GeoNamePairJob
from geo_dist_prep.utils import chunks
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "http://localhost:8080/ors/v2/directions/driving-car"


def call_api(pairs):
    client = httpx.Client(http2=True)

    results = []

    for i, pair in enumerate(pairs):
        if i % 1000 == 0:
            print("enrich: pair", i)
        params = {
            "start": f"{pair.lon1},{pair.lat1}",
            "end": f"{pair.lon2},{pair.lat2}",
        }
        response = None

        response = client.get(url, params=params).json()
        distance = -1.0

        if "error" in response:
            if response["error"]["code"] == 2004:
                # didn't configure the server to do 350km, only 100km
                continue
            if response["error"]["code"] == 2010:
                # one of the endpoints isn't in this data file
                continue
            if response["error"]["code"] == 2009:
                # no route found
                results.append(-1.0)
                continue

        try:
            distance = response["features"][0]["properties"]["summary"]["distance"]
            distance = float(distance) / 1000.0
        except Exception:
            print(json.dumps(response, indent=2))
            continue

        results.append(
            [
                pair.start_id,
                pair.end_id,
                pair.lat1,
                pair.lon1,
                pair.lat2,
                pair.lon2,
                distance,
            ]
        )

    return results


def enrich_country(country_code):
    print("enrich:", country_code)

    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    pair_job = (
        session.query(GeoNamePairJob)
        .filter(GeoNamePairJob.success, GeoNamePairJob.country_code == country_code)
        .all()
    )[0]

    print("enrich: enriching", country_code, "from pair job", pair_job.id)

    # job = GeoNameEnrichJob()
    # job.pair_job_id = pair_jobs[0].id
    # session.add(job)

    start_query = session.query(
        GeoName.osm_id.label("id1"),
        GeoName.lat.label("lat1"),
        GeoName.lon.label("lon1"),
    ).subquery()

    end_query = session.query(
        GeoName.osm_id.label("id2"),
        GeoName.lat.label("lat2"),
        GeoName.lon.label("lon2"),
    ).subquery()

    pairs = (
        session.query(
            GeoNamePair.id,
            GeoNamePair.job_id,
            GeoNamePair.start_id,
            GeoNamePair.end_id,
            start_query,
            end_query,
        )
        .filter(GeoNamePair.job_id == pair_job.id)
        .join(start_query, start_query.c.id1 == GeoNamePair.start_id)
        .join(end_query, end_query.c.id2 == GeoNamePair.end_id)
    )

    with ProcessPoolExecutor() as executor:
        for results in executor.map(call_api, chunks(pairs, 10_000)):
            for row in results:
                print("\t".join(row))


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


def main():
    pending_countries = get_pending_countries()
    print("enrich:", len(pending_countries), "left to go")

    groups = group_countries_by_region(pending_countries)

    for region, countries in groups.items():
        with running_docker_container(region):
            for country_code in countries:
                enrich_country(country_code)


if __name__ == "__main__":
    main()
    raise Exception("stop")
