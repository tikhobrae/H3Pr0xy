#!/bin/bash
read -p "Enter Command for run >>> " command
read -p "Enter time(s) >>> " time
allrun = 0
while true; do
    ((allrun++))
    echo "---------'$allrun'-----------"
    echo "Run"
    
    eval $command
    
    sleep $time
done
