#!/bin/sh
set -e

echo "Waiting for redis-src..."
until nc -z redis-src 6379; do
    sleep 1
done
echo "redis-src ready."

echo "Waiting for redis-dst..."
until nc -z redis-dst 6379; do
    sleep 1
done
echo "redis-dst ready."

echo "Migrating all data with RIOT..."
riot replicate --key-pattern "*" redis://redis-src:6379/0 redis://redis-dst:6379/0

echo "Migration done!"
tail -f /dev/null
