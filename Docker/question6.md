```
•COPY vs ADD ?

For a DevOps interview, remember this simple rule:

COPY copies files and directories. ADD can copy files too, but it has additional features such as extracting local tar archives and fetching remote URLs in supported Docker builders.

1. COPY                                      vs                                           ADD

Copies files and directories into the image.                 Copies files and directories, with additional features.
Simple and predictable.                                      Has extra behavior, such as extracting local tar archives.
Preferred for normal file copying.                           Use when its extra features are specifically needed.




2. Example Dockerfile

FROM ubuntu:latest

WORKDIR /app

COPY app.py .
COPY config/ ./config/

Here:

COPY app.py . copies app.py into /app.

COPY config/ ./config/ copies the config directory into /app/config/.

Example using ADD
ADD app.tar.gz /app/

When the local archive is a supported tar format, Docker automatically extracts it into /app.

3. Important interview points

COPY does not automatically extract tar archives.

ADD can automatically extract supported local tar archives.

For remote files, ADD behavior depends on the builder; prefer RUN curl or RUN wget when you need explicit download control.

For ordinary copying, follow Docker best practice and use COPY.

Interview answer to memorize

COPY is used to copy files and directories from the build context into a Docker image. ADD has similar functionality but also supports automatic extraction of local tar archives and, in supported builders, remote URL sources. I prefer COPY unless I specifically need ADD's extra features.