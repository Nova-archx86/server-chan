#!/bin/sh
# This script checks for required dependancies and starts the bot using a custom command
# 

echo "Checking for ffmpeg..."

if [[ -e /usr/bin/ffmpeg ]] || [[ -e /usr/local/bin/ffmpeg ]]
then
	echo "Starting..."
	nohup python3 bot.py &
else
	echo "ERROR! ffmpeg is not installed!"
fi

