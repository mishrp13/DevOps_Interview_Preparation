```
•CMD vs ENTRYPOINT?

or a DevOps interview, remember this simple difference:

ENTRYPOINT defines the main executable, while CMD provides default arguments or a default command.

1. CMD                                         vs                                         ENTRYPOINT

Provides a default command or arguments.                                Defines the main executable of the container.
Easily overridden when running docker run.                              Usually remains fixed when running docker run.
Used to specify default behavior.                                       Used to define what the container runs.



2. Example Dockerfile

FROM ubuntu:latest

ENTRYPOINT ["echo"]
CMD ["Hello World"]

Run the container:

docker run myimage

Output:

Hello World

Now override the default argument:

docker run myimage "Hello DevOps"

Output:

Hello DevOps

Why? ENTRYPOINT runs echo, and CMD supplies the default argument "Hello World". The text supplied to docker run replaces the default CMD arguments.

3. What if we use only CMD?
CMD ["echo", "Hello World"]

Running:

docker run myimage

Output:

Hello World

But running:

docker run myimage ls

runs ls instead of echo Hello World.

4. Interview answer to memorize

CMD provides the default command or arguments for a Docker container, and it can be overridden at runtime. ENTRYPOINT defines the main executable that runs when the container starts. When both are used in exec form, CMD typically supplies the default arguments to ENTRYPOINT.

Interview tip: Know the difference between overriding the command and overriding the arguments. This is the key concept interviewers often test.