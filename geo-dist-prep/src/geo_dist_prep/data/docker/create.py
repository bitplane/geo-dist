import json
import os

from .regions import REGIONS

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def set_source_files(config: dict, sources: list):
    config["ors"]["services"]["routing"]["sources"] = [
        "/home/ors/ors-core/data/" + source for source in sources
    ]


def create_dirs(path):
    # this is a hack. should run as correct user instead by setting GUI and UID
    for subdir in (
        "graphs/car",
        "logs/ors",
        "logs/tomcat",
        "data",
        "elevation_cache",
        "data/graphs",
        "conf",
    ):
        os.makedirs(os.path.join(path, subdir), exist_ok=True)


def create_docker_environments():
    with open(THIS_DIR + "/docker-compose.yml", "r") as fin:
        compose_file = fin.read()

    with open(THIS_DIR + "/ors-config.json", "r") as fin:
        config_file = json.load(fin)

    for region in REGIONS:
        path = ".cache/ors/" + region.name
        create_dirs(path)

        region_file_name = region.file.split("/")[-1]
        set_source_files(config_file, [region_file_name])

        with open(path + "/conf/ors-config.json", "w") as fout:
            json.dump(config_file, fout)

        compose_file = compose_file.replace(
            "{{REGION_NAME}}", region.name.replace("_", "-")
        )

        with open(path + "/docker-compose.yml", "w") as fout:
            fout.write(compose_file)

        os.system("wget " + region.file + " -P " + path + "/data/")


if __name__ == "__main__":
    create_docker_environments()
