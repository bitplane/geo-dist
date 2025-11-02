import os
import sys

import yaml

from .regions import REGIONS

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def download_and_verify_osm_file(url: str, data_dir: str):
    """Download OSM file and verify checksum. Delete file and exit on checksum failure."""
    filename = url.split("/")[-1]
    filepath = os.path.join(data_dir, filename)
    checksum_url = url + ".md5"
    checksum_file = filepath + ".md5"

    # Download the OSM file (with resume support)
    print(f"Downloading {url}...")
    if os.system(f"wget --continue {url} -P {data_dir}") != 0:
        print(f"Failed to download {url}")
        sys.exit(1)

    # Download the checksum file
    print(f"Downloading checksum from {checksum_url}...")
    if os.system(f"wget -O {checksum_file} {checksum_url}") != 0:
        print(f"Failed to download checksum file {checksum_url}")
        sys.exit(1)

    # Verify checksum
    print(f"Verifying checksum for {filename}...")
    original_dir = os.getcwd()
    try:
        os.chdir(data_dir)
        result = os.system(f"md5sum -c {filename}.md5")
        if result != 0:
            print(f"Checksum verification failed for {filename}")
            print("=== CHECKSUM FAILURE DETAILS ===")

            # Show expected checksum from .md5 file
            if os.path.exists(f"{filename}.md5"):
                with open(f"{filename}.md5", "r") as f:
                    expected_line = f.read().strip()
                print(f"Expected (from .md5 file): {expected_line}")
            else:
                print("ERROR: .md5 file not found!")

            # Show actual checksum of downloaded file
            if os.path.exists(filename):
                actual_result = os.popen(f"md5sum {filename}").read().strip()
                print(f"Actual (computed): {actual_result}")

                # Show file size for additional diagnostics
                file_size = os.path.getsize(filename)
                print(f"File size: {file_size} bytes")
            else:
                print("ERROR: Downloaded file not found!")

            print("=== END CHECKSUM DETAILS ===")
            print("Deleting corrupt file...")
            os.remove(filename)
            if os.path.exists(filename + ".md5"):
                os.remove(filename + ".md5")
            sys.exit(1)
        print(f"Checksum verification passed for {filename}")
    finally:
        os.chdir(original_dir)


def set_source_files(config: dict, sources: list):
    # Update for modern ORS config structure (v9.3.0+)
    if len(sources) == 1:
        config["ors"]["engine"]["profile_default"]["build"]["source_file"] = (
            "/home/ors/ors-core/data/" + sources[0]
        )
    else:
        # For multiple sources, use the first one
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
        config_file = yaml.safe_load(fin)

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

        download_and_verify_osm_file(region.file, path + "/data")


if __name__ == "__main__":
    create_docker_environments()
