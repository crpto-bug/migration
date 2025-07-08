
import redis
import os
import time
import json

def wait_for_redis(r):
    while True:
        try:
            r.ping()
            break
        except Exception:
            print("Waiting for Redis to be ready...")
            time.sleep(1)
    print("Connected to Redis.")

def seed_hashes(r):
    r.hset("employee:1", mapping={"name": "John", "age": "30", "dept": "Engineering"})
    r.hset("employee:2", mapping={"name": "Jane", "age": "32", "dept": "HR"})
    print("Seeded hashes.")

def seed_geo(r):
    r.geoadd("cities", (77.209, 28.6139, "Delhi"), (72.8777, 19.0760, "Mumbai"))
    print("Seeded geo data.")

def seed_bloom(r):
    try:
        r.execute_command("BF.RESERVE", "email_bf", 0.01, 1000)
        r.execute_command("BF.ADD", "email_bf", "john@example.com")
        r.execute_command("BF.ADD", "email_bf", "jane@example.com")
        print("Seeded Bloom filter.")
    except Exception as e:
        print("Bloom filter (module missing?):", e)

def seed_vector(r):
    r.hset("vec:1", mapping={"vector": ",".join(["0.1", "0.2", "0.3"])})
    print("Seeded vector (as CSV string).")

def seed_json(r):
    try:
        r.execute_command('JSON.SET', 'user:1', '$', json.dumps({"name": "Alice", "active": True}))
        print("Seeded JSON document.")
    except Exception as e:
        print("JSON (module missing?):", e)

def seed_graph(r):
    try:
        r.execute_command("GRAPH.QUERY", "social", "CREATE (:Person {name:'Bob',age:25})")
        print("Seeded Graph.")
    except Exception as e:
        print("Graph (module missing?):", e)

def seed_time_series(r):
    try:
        r.execute_command("TS.CREATE", "sensor:1", "RETENTION", 60000, "LABELS", "type", "temp")
        r.execute_command("TS.ADD", "sensor:1", "*", 25.3)
        r.execute_command("TS.ADD", "sensor:1", "*", 25.8)
        print("Seeded TimeSeries.")
    except Exception as e:
        print("TimeSeries (module missing?):", e)

def main():
    r = redis.Redis(
        host=os.getenv("REDIS_HOST", "redis-src"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True,
    )
    wait_for_redis(r)

    seed_hashes(r)
    seed_geo(r)
    seed_bloom(r)
    seed_vector(r)
    seed_json(r)
    seed_graph(r)
    seed_time_series(r)
    print("Seeding complete.")

if __name__ == "__main__":
    main()
