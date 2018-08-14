#!/bin/bash

#Give message when starting the container
printf "\n \n \n ------------------------Starting container ------------------------ \n \n \n"

# Configure user nobody to match unRAID's settings
#export DEBIAN_FRONTEND="noninteractive"
#usermod -u 99 nobody
#usermod -g 100 nobody
#usermod -d /home nobody
#chown -R nobody:users /home

    # url = sys.argv[1]
    # filename = sys.argv[2]
    # window_size = sys.argv[3]
    # user_agent = sys.argv[4]
    # wait_time = sys.argv[5]
    # refresh_delay = sys.argv[6]
    # log_level = sys.argv[7]

# Quit if these are not set
[ -z "${URL}" ] && echo "URL is not set" && exit 1
[ -z "${FILENAME}" ] && echo "Output FILENAME is not set" && exit 1
[ -z "${REFRESH_DELAY}" ] && echo "REFRESH_DELAY is not set" && exit 1

# test for empty variable
if [ -z "$WINDOW_SIZE" ]; then
WINDOW_SIZE="1200x800"
else
WINDOW_SIZE="${WINDOW_SIZE}"
fi

# test for empty variable
if [ -z "$USER_AGENT" ]; then
USER_AGENT="0"
else
USER_AGENT="${USER_AGENT}"
fi

# test for empty variable
if [ -z "$WAIT_TIME" ]; then
WAIT_TIME="0"
else
WAIT_TIME="${WAIT_TIME}"
fi

# test for empty variable
if [ -z "$LOG_LEVEL" ]; then
LOG_LEVEL="CRITICAL"
else
LOG_LEVEL="${LOG_LEVEL}"
fi

# Start program
python /tmp/screenshot.py $URL $FILENAME WINDOW_SIZE USER_AGENT WAIT_TIME $REFRESH_DELAY LOG_LEVEL

echo "Stopping Container.."
