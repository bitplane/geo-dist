#!/bin/bash

# for some reason Python won't pass these variables


UID=$(id -u)
GID=$(id -g)
export UID=$UID
export GID=$GID

docker-compose --file ".cache/ors/$1/docker-compose.yml" up | while read -r line; do
  echo "$line"
  if [[ "$line" == *"[routing.RoutingProfile] - [1] Finished at:"* ]]; then
    break
  fi
done

