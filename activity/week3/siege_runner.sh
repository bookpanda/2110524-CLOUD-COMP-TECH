#!/bin/bash

concurrency=10  # Starting value for concurrency (-c)
delay=1         # Delay between requests (-d)
repeats=1       # Number of repetitions (-r)
url="http://act3-paas-autoscale-5-env.eba-4ifhnppy.ap-southeast-1.elasticbeanstalk.com"
log_file="siege.log"

for i in {1..20}; do
    echo "Running siege with concurrency=$concurrency, delay=$delay, repeats=$repeats..."
    
    siege -c$concurrency -d$delay -r$repeats "$url" -l \
        -m="c=$concurrency, d=$delay, r=$repeats"
    
    concurrency=$((concurrency + 10))
    
    sleep 2
done

echo "Siege runs complete. Logs saved to $log_file."
