import os
import redis
from dotenv import load_dotenv

load_dotenv()

src = redis.Redis(
    host=os.getenv("SRC_HOST", "redis-src"),
    port=int(os.getenv("SRC_PORT", 6379)),
    password=os.getenv("SRC_PASS", None),
    db=int(os.getenv("SRC_DB", 0)),
    ssl=os.getenv("SRC_SSL", "").lower() in ("1", "true", "yes"),
    decode_responses=True
)
dst = redis.Redis(
    host=os.getenv("DST_HOST", "redis-dst"),
    port=int(os.getenv("DST_PORT", 6379)),
    password=os.getenv("DST_PASS", None),
    db=int(os.getenv("DST_DB", 0)),
    ssl=os.getenv("DST_SSL", "").lower() in ("1", "true", "yes"),
    decode_responses=True
)

def migrate_indexes():
    try:
        indexes = src.execute_command("FT._LIST")
        print(f"Found indexes: {indexes}")
        for idx in indexes:
            try:
                info = src.execute_command("FT.INFO", idx)
                # FT.INFO returns alternating key/val; convert to dict:
                info_dict = dict(zip(info[::2], info[1::2]))
                schema = info_dict.get('attributes', [])
                # Build FT.CREATE statement (simple version)
                args = [idx, "ON", info_dict['index_definition'][1], "SCHEMA"]
                for field in schema:
                    args.append(field[1])
                    args.extend(field[2:])  # type, options, etc
                print(f"Recreating index {idx}: {args}")
                try:
                    dst.execute_command("FT.CREATE", *args)
                except redis.ResponseError as e:
                    print(f"Index {idx} already exists or failed: {e}")
            except Exception as e:
                print(f"Error migrating index {idx}: {e}")
    except Exception as e:
        print(f"No FT indexes to migrate or error: {e}")

if __name__ == "__main__":
    migrate_indexes()
