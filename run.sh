#!/bin/bash

# Prompt user for command and time interval
read -p "Enter Command for run >>> " command
read -p "Enter time(s) >>> " time

# Initialize a counter for runs
allrun=0

# Infinite loop
while true; do
    ((allrun++))  # Increment the counter
    echo "---------'$allrun'-----------"  # Display the count
    echo "Run"

    # Execute the command
    eval "$command"

    # Wait for the specified time
    sleep "$time"
done
