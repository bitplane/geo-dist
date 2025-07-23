import json
import os

import yaml

from .regions import REGIONS

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def set_source_files(config: dict, sources: list):
    # Update for new ORS config structure
    if len(sources) == 1:
        config["ors"]["engine"]["profile_default"]["build"]["source_file"] = (
            "/home/ors/ors-core/data/" + sources[0]
        )
    else:
        # For multiple sources, we'd need a different approach
        # For now, just use the first one
        config["ors"]["engine"]["profile_default"]["build"]["source_file"] = (
            "/home/ors/ors-core/data/" + sources[0]
        )


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
        compose_file_template = fin.read()

    with open(THIS_DIR + "/ors-config.json", "r") as fin:
        config_file = json.load(fin)

    for region in REGIONS:
        if region.too_large:
            print("Skipping", region.name, "due to insufficient RAM")
            continue

        path = ".cache/ors/" + region.name
        create_dirs(path)

        region_file_name = region.file.split("/")[-1]
        set_source_files(config_file, [region_file_name])

        with open(path + "/conf/ors-config.yml", "w") as fout:
            yaml.dump(config_file, fout, default_flow_style=False, indent=2)

        compose_file = (
            compose_file_template.replace(
                "{{REGION_NAME}}", region.name.replace("_", "-")
            )
            .replace("{{RAM}}", str(region.ram))
            .replace("{{RAM_75}}", str(int(region.ram * 0.75)))
            .replace("{{RAM_95}}", str(int(region.ram * 0.95)))
        )

        with open(path + "/docker-compose.yml", "w") as fout:
            fout.write(compose_file)

        os.system("wget --continue " + region.file + " -P " + path + "/data/")


if __name__ == "__main__":
    create_docker_environments()
