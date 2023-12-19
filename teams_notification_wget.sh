#!/bin/bash

wget --method=POST --header="Content-type: application/json" --body-data '{"text":"'"$1"'"}' $2
