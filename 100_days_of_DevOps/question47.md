```
A python app needed to be Dockerized, and then it needs to be deployed on App Server 3. We have already copied a requirements.txt file (having the app dependencies) under /python_app/src/ directory on App Server 3. Further complete this task as per details mentioned below:



Create a Dockerfile under /python_app directory:

Use any python image as the base image.
Install the dependencies using requirements.txt file.
Expose the port 5001.
Run the server.py script using CMD.

Build an image named nautilus/python-app using this Dockerfile.


Once image is built, create a container named pythonapp_nautilus:

Map port 5001 of the container to the host port 8099.

Once deployed, you can test the app using curl command on App Server 3.


sol:
Step 1: Connect to App Server 3
SSH into App Server 3 using the credentials provided in your environment.
ssh banner@stapp03


Step 2: Create the Dockerfile
Navigate to /python_app:
cd /python_app


Create the Dockerfile:
vi Dockerfile


Add the following content:

FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5001

CMD ["python", "server.py"]



Explanation:
- FROM: Uses Python 3.11 as the base image.
- WORKDIR: Sets /app as the working directory inside the container.
- COPY src/requirements.txt .: Copies the dependency file.
- RUN: Installs Python dependencies.
- COPY src/ .: Copies application files, including server.py.
- EXPOSE 5001: Documents the application's port.
- CMD: Starts the Python application.
Step 3: Build the Docker image
Run this command from /python_app:
docker build -t nautilus/python-app .


Verify the image:
docker images


You should see an image named nautilus/python-app.
Step 4: Create and start the container
Run:
docker run -d \
  --name pythonapp_nautilus \
  -p 8099:5001 \
  nautilus/python-app


This command:
- Creates a container named pythonapp_nautilus.
- Runs it in detached mode (-d).
- Maps host port 8099 to container port 5001.
Step 5: Verify the deployment
Check whether the container is running:
docker ps


Expected output will resemble:
CONTAINER ID   IMAGE                 PORTS                    NAMES
abc123def456   nautilus/python-app   0.0.0.0:8099->5001/tcp   pythonapp_nautilus


Test the application:
curl http://localhost:8099


If the application has started successfully and serves the root endpoint, you should receive an HTTP response from the Python application.

If it fails, check the container logs:
docker logs pythonapp_nautilus


Important: Ensure server.py listens on 0.0.0.0:5001, not 127.0.0.1:5001, inside the container.

For example, with Flask:
app.run(host="0.0.0.0", port=5001)



Step 6: Final verification
Run:
docker inspect pythonapp_nautilus --format '{{.State.Status}}'


Expected output:
running


Quick command summary

cd /python_app

cat > Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
EXPOSE 5001
CMD ["python", "server.py"]
EOF

docker build -t nautilus/python-app .

docker run -d \
  --name pythonapp_nautilus \
  -p 8099:5001 \
  nautilus/python-app

docker ps

curl http://localhost:8099



This completes all four requested deployment steps, assuming the build succeeds and the application listens on port 5001. These commands need to be executed on App Server 3; I haven't executed them on your server.
