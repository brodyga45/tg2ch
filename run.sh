#!/bin/bash
tmux new -d -s bot

Help()
{
   # Display Help
   echo "Syntax: sh run.sh [-h|-r]"
   echo "options:"
   echo "r     Restart the bot."
   echo "h     Print this Help."
   echo
}

while getopts ":rh" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      r) # Restart bot
         tmux send-keys -t bot ^c;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

tmux send-keys -t bot C-u
tmux send-keys -t bot 'python3 main.py'
tmux send-keys ENTER