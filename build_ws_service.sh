#!/bin/bash

cd ws_server_image_src && docker build -t ws_server .

docker swarm leave -f
docker swarm init --advertise-addr $(hostname -I | cut -d' ' -f1)
