import json
import subprocess
import time
from contextlib import contextmanager

import httpx


@contextmanager
def running_docker_container(container_name):
    try:
        subprocess.run(["./build/docker-up.sh", container_name])

        t = 1
        while True:
            try:
                response = httpx.get(
                    "http://localhost:8080/ors/v2/directions/driving-car"
                ).json()
                if "error" in response and response["error"]["code"] == 2001:
                    # our invald response was served, so the server is up
                    break
                else:
                    # Unexpected response, so wait a bit and try again.
                    # Print it so we can deal with other conditions here later.
                    print(response)
                    time.sleep(t)
                    t += 2

            except (httpx.HTTPError, json.decoder.JSONDecodeError):
                print(f"Waiting {t}s for {container_name}...")
                time.sleep(t)
                t += 2

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
