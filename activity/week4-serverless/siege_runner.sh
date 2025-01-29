#!/bin/bash

concurrency=5  # Starting value for concurrency (-c)
delay=1         # Delay between requests (-d)
repeats=1       # Number of repetitions (-r)
url='https://szzhh8og17.execute-api.ap-southeast-1.amazonaws.com/default/act4 POST {"a": "2", "b": 3, "op": "*"}'
log_file="siege.log"

for i in {1..40}; do
    echo "Running siege with concurrency=$concurrency, delay=$delay, repeats=$repeats..."
    
    siege -c$concurrency -d$delay -r$repeats --content-type "application/json" "$url" -l \
        -m="c=$concurrency, d=$delay, r=$repeats"
    
    concurrency=$((concurrency + 5))
    
    sleep 2
done

echo "Siege runs complete. Logs saved to $log_file."