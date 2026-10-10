```
•How do you pass environment variables (-e, --env-file)?

In Docker, environment variables are used to pass configuration values to a container at runtime without hardcoding them into the Docker image.

There are two common ways to pass environment variables when running a container:

1. `-e` or `--env`: Used to pass individual environment variables directly through the Docker command.
2. `--env-file`: Used to load multiple environment variables from a file.

For example, we can pass database configuration, application ports, and environment names using environment variables.

This approach makes Docker images reusable across development, testing, and production environments because the configuration can change without rebuilding the image.

However, environment variables are not a secure secrets-management solution by themselves. Sensitive credentials should be handled carefully and, where appropriate, managed through a dedicated secrets-management system.

