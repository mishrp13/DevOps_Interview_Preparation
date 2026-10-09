```
•What is the difference between docker stop and docker kill?


In a DevOps interview, the main difference between docker stop and docker kill is how they terminate a running container.

1. Difference between docker stop and docker kill

Feature                        Docker stop                                   Docker kill
Purpose                      Gracefully stops a container               Forcefully stops a container by default
Signal sent                    Sends SIGTERM first                           Sends SIGKILL by default
Shutdown time                Waits for a grace period                    Stops immediately by default
Application cleanup       Allows the app to finish tasks and clean up    Usually doesn't allow cleanup
Timeout              Default is 10 seconds on Linux, 30 seconds on Windows  No graceful shutdown timeout by default
Data safety                 Better for normal shutdowns            Higher risk of incomplete writes or unfinished tasks
Best use case             Routine deployments and maintenance                Hung or unresponsive containers


2. How docker stop works

Command:

docker stop mycontainer

1. Send SIGTERM

Ask the application to shut down gracefully.

2. Wait for the grace period

The app can finish requests, close connections, and flush data.

3. Send SIGKILL if still running

Docker forcefully terminates the container after the timeout.

You can specify the timeout:

docker stop -t 30 mycontainer

This gives the container up to 30 seconds to shut down gracefully before Docker sends SIGKILL.

DevOps example: During a production deployment, you stop an old application container so it can finish processing requests before being replaced by a new version.

3. How docker kill works

Command:

docker kill mycontainer

Docker sends SIGKILL by default, terminating the container's main process without giving it a graceful shutdown period.

You can also specify a different signal:

docker kill --signal=SIGTERM mycontainer

This sends SIGTERM instead of the default SIGKILL. The process may handle the signal gracefully, depending on its implementation.

DevOps example: An application container is stuck and does not respond to normal shutdown. You use docker kill to terminate it immediately.

4. Practical demonstration

Run a test container:

docker run -d --name test-app nginx

Stop it gracefully:

docker stop test-app

Start it again:

docker start test-app

Forcefully terminate it:

docker kill test-app

Check its status:

docker ps -a

The container will normally show as Exited after either command. The difference is the shutdown process, not the final container status.

5. Common DevOps interview questions

Q1. Which command is preferred in production: docker stop or docker kill?

docker stop is preferred because it allows the application to shut down gracefully, complete in-flight requests, and release resources. Use docker kill when immediate termination is necessary.

Q2. What happens if a container does not stop within the timeout?

Docker sends SIGKILL to terminate it. You can increase the timeout using docker stop -t 30 container_name.

Q3. Does docker kill delete the container?

No. It terminates the running container but does not remove it. To remove a stopped container, use:

docker rm mycontainer

Q4. Does docker stop guarantee that no data will be lost?

No. It gives the application an opportunity to shut down cleanly, but data safety depends on how the application handles termination, persists data, and completes writes.

Q5. What is the difference between docker kill and kill -9?

docker kill targets a Docker container's main process by default, using SIGKILL.

kill -9 PID sends SIGKILL to a specific process ID in the current process namespace.

6. Best interview answer to memorize
Writing

docker stop and docker kill are used to stop running Docker containers, but they differ in their termination behavior.

docker stop sends SIGTERM first, allowing the application to shut down gracefully. If the container does not stop within the configured timeout, Docker sends SIGKILL.

docker kill sends SIGKILL by default, terminating the container's main process immediately without waiting for graceful shutdown.

In production environments, I prefer docker stop during deployments and maintenance because it allows in-flight requests and cleanup tasks to complete. I use docker kill when a container is unresponsive or needs immediate termination.

Quick memory trick: stop = graceful first; kill = forceful by default.
