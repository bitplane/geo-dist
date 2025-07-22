#!/bin/bash

# for some reason Python won't pass these variables
# UID is readonly in bash, so we unset it first

USER_ID=$(id -u)
GROUP_ID=$(id -g)

env -u UID UID="$USER_ID" GID="$GROUP_ID" docker-compose --file ".cache/ors/$1/docker-compose.yml" up | while read -r line; do
  echo "$line"
  if [[ "$line" == *"] Finished at:"* ]]; then
    break
  fi
done

