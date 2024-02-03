#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
./trellobot.py &

# Start the webhook checking and creating
./webhook_generate.py


# now we bring the primary process back into the foreground
# and leave it there
fg %1