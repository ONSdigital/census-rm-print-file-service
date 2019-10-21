#!/usr/bin/env bash
echo "Waiting for [print-file-service] to be ready"
max_attempts=30
attempt=0
while true; do
    response=$(docker inspect dev-print-file-service -f "{{ .State.Health.Status }}")
    if [[ "$response" == "healthy" ]]; then
        echo "[print-file-service] is ready"
        break
    fi

    echo "[print-file-service] not ready ([$response] is its current state)"
    attempt=$(attempt + 1)
    if ((attempt > max_attempts )); then
      echo "[print-file-service] failed to start"
      exit 1
    fi
    sleep 2s

done

echo "Containers running and alive"
