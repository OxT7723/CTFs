#!/bin/bash
docker rm -f web_trial_by_fire
docker build --tag=web_trial_by_fire .
docker run -p 1337:1337 -it --name=web_trial_by_fire web_trial_by_fire