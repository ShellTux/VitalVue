FROM postgres:16-alpine

USER postgres

ARG PG_SELECT_COMMAND="SELECT 1 FROM pg_database WHERE datname = 'main'"
ARG PG_CREATE_DATABASE_COMMAND="CREATE DATABASE main"
ARG PG_USER_COMMAND="ALTER USER postgres WITH ENCRYPTED PASSWORD 'mysecurepassword';"

RUN chmod 0700 /var/lib/postgresql/data \
    && initdb /var/lib/postgresql/data \
    && echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf \
    && echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf \
    && pg_ctl start \
    && psql --username=postgres --tuples-only --command="${PG_SELECT_COMMAND}" \
    | grep -q 1 \
    || psql --username=postgres --command="${PG_CREATE_DATABASE_COMMAND}" \
    && psql --command="${PG_USER_COMMAND}"

EXPOSE 5432
