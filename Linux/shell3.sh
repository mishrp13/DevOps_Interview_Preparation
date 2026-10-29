#!/bin/bash

services= ("nginx", "ssh", "docker")

echo "---------------------------------"
echo "Service-Health-Check-Report"
echo "----------------------------------"

for service in "${services[@]}" ; do
     if systemctl is-active --quiet "$service"; then
           echo "$service is running"
     else
        echo "$service is Stopped"
        echo "Attempting to restart $service"
        sudo systemctl restart "$service"
        if systemctl is-active --quiet "$service"; then
           echo "$service has been restarted successfully"
        else
           echo "Failed to restart $service check logs"
        fi 
    fi


    echo "--------------------------------------------------"
done

