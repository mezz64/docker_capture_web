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


# Start program
python screenshot.py $URL $FILENAME $WINDOW_SIZE $USER_AGENT $WAIT_TIME $REFRESH_DELAY $LOG_LEVEL

echo "Stopping Container.."
