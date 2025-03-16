#!/bin/bash

# create Docker network
docker network create data_engineering

# Start the containers.
# The -f flag is used to specify the location of the docker-compose file.
# The --build flag is used to build the image before starting the container.
# It is recommended to use --build to ensure the same version of the image is used, especially if running for the first time.
# The -d flag is used to run the containers in the background.
# If you have already built the image and just want to start the container, you can omit the --build flag. for the command below.

# Start Airflow for the first time, you can just use -d if you have already built the image.
docker compose -f ./docker/airflow/docker-compose.yml up --build -d 


# Start postgres for the first time, you can just use -d if you have already built the image.
docker compose -f ./docker/postgres/docker-compose.yml up --build -d

# Start superset for the first time, you can just use -d if you have already built the image.
docker compose -f ./docker/superset/docker-compose.yml up --build -d
