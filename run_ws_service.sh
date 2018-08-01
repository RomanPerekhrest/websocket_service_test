#!/bin/bash

# deploying service as a distributed load-balanced application
docker stack deploy -c compose_files/ws-service-compose.yml ws_service
