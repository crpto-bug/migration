# Redis Data Seeding and Migration.

This project demonstrates a fully automated workflow for:
- **Seeding** a Redis Stack with different data types (hash, geo, bloom filter, vector, JSON, etc.) via Python.
- **Migrating** all data (including Redis modules) from a source Redis to a destination Redis.

All steps run via **Docker Compose**.

---

## Project Structure


├── docker-compose.yaml # Service definitions

├── Dockerfile # Python environment

├── requirements.txt # Python dependencies

├── seed_data.py # Python script: seeds data into source Redis

├── riot_migrate.sh # Shell script: runs migration using RIOT


---

## How It Works

1. **Source Redis** (`redis-src`) and **Destination Redis** (`redis-dst`) are started as Redis Stack containers.
2. **Seeder service** (Python-based) waits for source Redis to be ready and then seeds various data types.
3. **RIOT migrator service** waits for both Redis instances, then migrates **all data** (including modules) from `redis-src` to `redis-dst` .
4. At the end, both the seeded and migrated data can be verified using `redis-cli`.

---

## Files Explained

| File                | Purpose                                                                 |
|---------------------|-------------------------------------------------------------------------|
| `docker-compose.yaml` | Orchestrates all containers: source Redis, destination Redis, seeder and migrator. |
| `Dockerfile`        | Python image for the seeding.                                    |
| `requirements.txt`  | Lists Python dependencies for the seeder.                               |
| `seed_data.py`      | Seeds hashes, geo, bloom filter, vectors, JSON, etc. into `redis-src`.  |
| `riot_migrate.sh`   | Waits for both Redis servers, then migrates all data via RIOT.          |

---

## How To Run

> **Prerequisites:**  
> - [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed

1. **Clone the repository** (or copy the files into a directory).

2. **Ensure `riot_migrate.sh` is executable:**
   ```sh
   chmod +x riot_migrate.sh
3. ** Run the command `docker compose up --build` **
