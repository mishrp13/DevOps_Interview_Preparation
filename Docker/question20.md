```
•depends_on: does it wait for the service to be ready?

Short answer: No, not by default. It controls the startup order of services. To wait for a dependency to become healthy, use condition: service_healthy with a healthcheck.


In Docker Compose, `depends_on` is used to define dependencies between services and control their startup order.

By default, Docker Compose starts the dependency before starting the dependent service, but it does not wait for the dependency to be fully ready to handle requests.

For example, if an application depends on a MySQL database, Compose may start the MySQL container first, but MySQL might still be initializing when the application starts.

To solve this problem, we configure a health check for the database and use `condition: service_healthy` in `depends_on`. This tells Docker Compose to wait until the database health check passes before starting the application.

Therefore, `depends_on` alone controls startup order, while `depends_on` combined with `service_healthy` can ensure the dependency is healthy before the dependent service starts.


****************************************************************************
services:
  app:
    image: myapp:latest
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db
      DB_PORT: "3306"

  db:
    image: mysql:8.4
    environment:
      MYSQL_ROOT_PASSWORD: example123
      MYSQL_DATABASE: appdb
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s

**********************************************************
How this works:
1. Compose starts the db service.
2. MySQL initializes.
3. Docker runs the configured health check.
4. Once MySQL reports healthy, Compose starts the app service.
***************************************************************