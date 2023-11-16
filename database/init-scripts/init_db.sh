#!/bin/bash

set -e
set -x

# Run the initial commands
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL

if [ -f /docker-entrypoint-initdb.d/initialize.sql ]; then
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -a -f /docker-entrypoint-initdb.d/initialize.sql
fi

echo "Script finished!"

set +x