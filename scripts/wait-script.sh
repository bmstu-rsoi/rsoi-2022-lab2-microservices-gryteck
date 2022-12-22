#!/usr/bin/env bash

IFS=", " read -ra ENDPOINTS <<<"$WAIT_ENDPOINTS"
path=$(dirname "$0")

PIDs=()
for endpoint in "${ENDPOINTS[@]}"; do
  "$path"/wait-for.sh -t 720 "$endpoint" -- echo "Endpoint $endpoint is up" &
  PIDs+=($!)
done

for pid in "${PIDs[@]}"; do
  if ! wait "${pid}"; then
    exit 1
  fi
done
