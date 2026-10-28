```
 44. 

 The Nautilus application development team shared static website content that needs to be hosted on the httpd web server using a containerised platform. The team has shared details with the DevOps team, and we need to set up an environment according to those guidelines. Below are the details:



a. On App Server 2 in Stratos DC create a container named httpd using a docker compose file /opt/docker/docker-compose.yml (please use the exact name for file).


b. Use httpd (preferably latest tag) image for container and make sure container is named as httpd; you can use any name for service.


c. Map 80 number port of container with port 8087 of docker host.


d. Map container's /usr/local/apache2/htdocs volume with /opt/data volume of docker host which is already there. (please do not modify any data within these locations).


sol:


To complete this task, create a Docker Compose file on App Server 2 in Stratos DC that runs an Apache HTTP Server container named httpd.
Step 1: SSH into App Server 2
ssh steve@stapp02


Enter the password when prompted.
Step 2: Create the Docker Compose directory
sudo mkdir -p /opt/docker


Step 3: Create the Docker Compose file
Open the file:
sudo vi /opt/docker/docker-compose.yml


Add the following content:
services:
  web:
    image: httpd:latest
    container_name: httpd
    ports:
      - "8087:80"
    volumes:
      - /opt/data:/usr/local/apache2/htdocs
    restart: unless-stopped


Configuration explained:
Setting	       Value
Service name	web
Docker image	httpd:latest
Container name	httpd
Host port	    8087
Container port	 80
Host volume	     /opt/data
Container volume	/usr/local/apache2/htdocs

The bind mount uses the existing /opt/data directory without modifying its contents.
Step 4: Start the container
Run:
cd /opt/docker
sudo docker compose -f docker-compose.yml up -d


If your server uses the older standalone Compose command, run:
sudo docker-compose -f docker-compose.yml up -d


Step 5: Verify the container
Check whether the container is running:
sudo docker ps


Expected output (similar to):
CONTAINER ID   IMAGE          PORTS                  NAMES
xxxxxxxxxxxx   httpd:latest   0.0.0.0:8087->80/tcp   httpd


Verify the port mapping:
sudo docker port httpd


Expected output:
80/tcp -> 0.0.0.0:8087


Test the HTTP server:
curl http://localhost:8087


This should return the website content from /opt/data, provided the directory contains a valid website entry point.
Step 6: Verify the volume mount
sudo docker inspect httpd --format '{{json .Mounts}}'


Confirm that:
- Source is /opt/data
- Destination is /usr/local/apache2/htdocs
- Mount type is bind
Final verification
Docker Compose file: /opt/docker/docker-compose.yml

Container name: httpd

Image: httpd:latest

Port mapping: 8087:80

Volume mapping: /opt/data:/usr/local/apache2/htdocs


Result: Once these commands complete successfully, the Apache HTTP Server container will be running on App Server 2 and serving the existing static website content through port 8087, without changing the website files.

