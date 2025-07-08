import redis
import os
import time

def wait_for_redis(r, name):
    while True:
        try:
            r.ping()
            break
        except Exception:
            print(f"Waiting for {name} Redis to be ready...")
            time.sleep(1)
    print(f"{name} connected.")

def migrate_all_keys(src, dst):
    keys = src.keys('*')
    print(f"Found {len(keys)} keys to migrate.")
    for k in keys:
        t = src.type(k).decode() if hasattr(src.type(k), "decode") else src.type(k)
        if t == "string":
            v = src.get(k)
            dst.set(k, v)
        elif t == "hash":
            v = src.hgetall(k)
            dst.hset(k, mapping=v)
        elif t == "list":
            v = src.lrange(k, 0, -1)
            if v:
                dst.delete(k)
                dst.rpush(k, *v)
        elif t == "set":
            v = src.smembers(k)
            if v:
                dst.delete(k)
                dst.sadd(k, *v)
        elif t == "zset":
            v = src.zrange(k, 0, -1, withscores=True)
            if v:
                dst.delete(k)
                dst.zadd(k, dict(v))
        else:
            print(f"Skipping key {k} of type {t} (use RIOT for modules)")

    print("Basic migration done.")

def main():
    src = redis.Redis(host=os.getenv("SRC_HOST", "redis-src"), port=int(os.getenv("SRC_PORT", 6379)), decode_responses=True)
    dst = redis.Redis(host=os.getenv("DST_HOST", "redis-dst"), port=int(os.getenv("DST_PORT", 6379)), decode_responses=True)
    wait_for_redis(src, "source")
    wait_for_redis(dst, "destination")
    migrate_all_keys(src, dst)

if __name__ == "__main__":
    main()
