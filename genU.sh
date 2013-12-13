#!/bin/bash

for i in $(seq 1 100)
do
    python manage.py generateUser $(echo 'john_doe_'$i) 'john' 'doe'
done