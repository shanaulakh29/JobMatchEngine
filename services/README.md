# API Quickstart

Boot Up All Microservices (Run In Virtual Env!!)
```bash
./run_services.sh
```

# Docker Container Quickstart

Start the full stack (build images and run containers):

```bash
docker compose up --build
```

Accessing PostgreSQL

```bash
docker exec -it my_postgres bash   # or 'sh' if bash isn't available
```

Then run psql from inside the container (uses environment vars provided to the container):

```bash
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
# or, if you prefer the postgres superuser
psql -U postgres
```

If you don't know the values of `POSTGRES_USER` or `POSTGRES_DB`, check your compose file or the `.env` file used by `docker compose`:

Accessing Redis

Open a shell in the Redis container (example name: `my_redis`):

```bash
docker exec -it my_redis sh
# then run the Redis CLI inside the container
redis-cli
```

Helpful docker-compose commands:

```bash
# Show running services
docker compose ps

# Tail logs for all services
docker compose logs -f

# Stop and remove containers, networks, and volumes created by compose
docker compose down
```






