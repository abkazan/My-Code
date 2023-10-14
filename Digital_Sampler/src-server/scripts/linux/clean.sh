#! /bin/bash

# Stop all containers
containers=$(docker ps -q)
if [[ ! -z $containers ]]; then
  docker kill $containers;
fi

# Remove all contianers
stopped_containers=$(docker ps -a -q)
if [[ ! -z $stopped_containers ]]; then
  docker rm $stopped_containers;
fi

# clear cache
rm -r ../../cache/*;

# clear screen
clear;

