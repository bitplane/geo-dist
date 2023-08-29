import json
import subprocess
import time
from contextlib import contextmanager

import httpx


@contextmanager
def running_docker_container(container_name):
    try:
        subprocess.run(["./build/docker-up.sh", container_name])

        while True:
            try:
                httpx.get("http://localhost:8080/ors/v2/directions/driving-car").json()
                break
            except (httpx.HTTPError, json.decoder.JSONDecodeError):
                print(f"Waiting for {container_name}...")
                time.sleep(5)

        print("Ready")
        yield

    finally:
        subprocess.run(
            [
                "docker-compose",
                "-f",
                f".cache/ors/{container_name}/docker-compose.yml",
                "down",
            ]
        )
