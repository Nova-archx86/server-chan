#!/bin/bash
# This script checks for required dependancies and starts the bot using a custom command
# 

echo "Checking for ffmpeg..."

if [[ -e /usr/bin/ffmpeg ]] || [[ -e /usr/local/bin/ffmpeg ]]
then
	
	if pgrep -fx 'python3 bot.py' >/dev/null
	then
		echo "ERROR bot is already running exiting..."
		exit 1
	else
		echo "Starting..."	
		nohup python3 bot.py &
	fi

else
	echo "ERROR! ffmpeg is not installed!"
fi

