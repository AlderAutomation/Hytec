#!/bin/bash

curl -X POST -H "Content-type: application/x-www-form-urlencoded" --data '{"text":"'"$1"'"}' $2
