#!/bin/bash
set -x
set -e

CONFIG_PATH=/data/options.json

# possible options for processing
MQTT_SERVER=$(jq --raw-output '.server' $CONFIG_PATH)
MQTT_PORT=$(jq --raw-output '.port' $CONFIG_PATH)
TOPIC=$(jq --raw-output '.topic' $CONFIG_PATH)
USER=$(jq --raw-output '.user' $CONFIG_PATH)
PASSWORD=$(jq --raw-output '.password' $CONFIG_PATH)

# read data
while read -r message
do
  echo $message
  for blind in 1 2 3 4 5 6 7 8; do
    if [ "$message" == "$blind|on" ]; then
        python /blinds.py $blind close || true
    fi
    if [ "$message" == "$blind|off" ]; then
        python /blinds.py $blind open || true
    fi
  done

done < <(mosquitto_sub -h "$MQTT_SERVER" -p "$MQTT_PORT" -u "$USER" -P "$PASSWORD" -t "$TOPIC" -q 1)
