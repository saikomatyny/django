#!/bin/bash

while true
do
    git add .
    git commit -m "Auto commit at $(date)"
    git push origin master
    inotifywait -r -e modify,create,delete .
done

