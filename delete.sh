#!/bin/bash

Help()
{
   # Display Help
   echo "Syntax: sh delete.sh [-f|-b|-h] [ids to delete separated by space]"
   echo "options:"
   echo "f     Delete requests"
   echo "b     Delete bugs"
   echo
}

while getopts ":fbh" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      f) # Feature
         for var in "$@"
         do
             rm ./frequests/$var
         done
         exit;;
      b) # Feature
         for var in "$@"
         do
             rm ./bags/$var
         done
         exit;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

