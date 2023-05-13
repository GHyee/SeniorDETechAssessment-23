FROM postgres:9.6

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD mysecretpassword
ENV POSTGRES_DB ecommerce

COPY sql_queries/create_tables.sql /docker-entrypoint-initdb.d/
