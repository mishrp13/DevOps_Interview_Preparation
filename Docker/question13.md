```
•How do you handle secrets? (Never bake them into images; use runtime env vars, secrets managers, build secrets)

In a DevOps interview, the most important rule for handling secrets is: Never hardcode secrets into a Dockerfile, bake them into a Docker image, or commit them to Git. Inject them securely at runtime or use a secrets manager.

Secrets include database passwords, API keys, access tokens, SSH private keys, cloud credentials, and TLS certificates.

1. Why should you never bake secrets into Docker images?

Consider this insecure Dockerfile:

FROM python:3.12-slim

WORKDIR /app

ENV DB_PASSWORD="MySecret123"

COPY . .

CMD ["python", "app.py"]

This is dangerous because:

The secret may be exposed through image configuration or inspection.

Anyone with access to the image may be able to retrieve it.

If the image is pushed to Docker Hub or a private registry, the secret may be distributed with it.

Deleting the secret in a later Dockerfile instruction does not reliably remove it from earlier image layers.

Secrets committed to Git may remain in repository history even after the file is edited.

Interview takeaway: A private Docker registry does not make hardcoded secrets safe.

2. Three secure ways to handle secrets

Method 1: Runtime environment variables

Pass secrets when starting the container instead of storing them in the image.

docker run -d \
  --name myapp \
  --env-file /secure/path/app.env \
  myapp:latest

Example contents of app.env:

DB_HOST=db.example.internal
DB_PASSWORD=your-secret-value

Keep this file out of Git and restrict its filesystem permissions.

Best for: Simple deployments, local development, and basic runtime configuration.

Limitation: Environment variables can be exposed through process inspection, debugging tools, or container configuration. Protect access to the Docker daemon and host.

Method 2: Secrets managers

Store credentials in a dedicated service and grant applications access only when needed.

Examples include AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, and Google Cloud Secret Manager.

Typical flow:

Secrets manager
Authenticated workload retrieves secret
Application uses the credential

Best for: Production applications, cloud deployments, credential rotation, auditing, and centralized access control.

Method 3: BuildKit build secrets

Sometimes a secret is needed during the image build—for example, to download a private package. Use a build secret rather than ARG or ENV.

Dockerfile:

# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

RUN --mount=type=secret,id=pip_conf \
    PIP_CONFIG_FILE=/run/secrets/pip_conf \
    pip install private-package

COPY . .

CMD ["python", "app.py"]

Build command:

docker build \
  --secret id=pip_conf,src=./pip.conf \
  -t myapp:latest .

BuildKit mounts the secret temporarily for that RUN instruction rather than automatically storing it in the resulting image layer.

Best for: Private package registries, authenticated dependency downloads, and secure build pipelines.

Important: Do not print the secret, copy it elsewhere, or save it in build logs or generated artifacts.

Example of what not to do:

ARG API_TOKEN
ENV API_TOKEN=$API_TOKEN

Passing a secret using --build-arg is not a secure secret-management mechanism. Build arguments and environment variables can be exposed through image metadata, build records, or other inspection mechanisms.

Use BuildKit secret mounts for secrets required during builds, and use a secrets manager or secure runtime injection for secrets required by the application.

4. How do you handle secrets in a DevOps CI/CD pipeline?

A typical production workflow looks like this:

1. Developer commits code

No passwords or API keys in Git.

2. CI/CD pipeline builds the image

BuildKit secrets are used if private dependencies require authentication.

3. Image is pushed to the registry

The image contains application artifacts, not credentials.

4. Application is deployed

Runtime credentials are retrieved or mounted securely.

In Kubernetes, you can use Kubernetes Secrets, preferably with encryption at rest, restrictive RBAC, and an external secrets manager where appropriate. For higher-security environments, avoid passing credentials through broadly accessible environment variables when a mounted secret or direct secret-manager integration is suitable.

Remember that Kubernetes Secrets are not automatically encrypted in etcd by default in every configuration, and base64 encoding is not encryption.

5. Common DevOps interview follow-up questions

Q1. What if a developer accidentally commits an API key to Git?

Revoke or rotate the exposed key immediately, remove it from the repository where appropriate, check logs and access history for misuse, and update the application to retrieve the replacement securely. Deleting the line from the latest commit alone is not enough.

Q2. Are Docker environment variables secure?

Not inherently. They are better than baking secrets into an image, but users with sufficient host or Docker-daemon access may be able to inspect them. Use access controls and consider mounted secrets or direct secrets-manager integration.

Q3. What is the difference between build-time and runtime secrets?

Build-time secrets are needed to create the image, such as credentials for a private package registry.

Runtime secrets are needed while the application runs, such as a database password.

Use BuildKit secret mounts for the first and a secrets manager or secure runtime injection for the second.

Q4. How do you rotate secrets in production?

Generate a new credential, update the secrets manager, ensure the application can reload it or redeploy the workload, verify the new credential works, and revoke the old credential when safe. Rotation procedures depend on the service and whether it supports overlapping credentials.

6. Best interview answer to memorize
Writing

In DevOps, I never hardcode secrets in a Dockerfile or commit them to Git because they can leak through image layers, metadata, source history, or container inspection.

For runtime secrets, I use a secrets manager such as AWS Secrets Manager or HashiCorp Vault, or securely inject secrets into the container at deployment time.

For build-time secrets, such as credentials for a private package registry, I use Docker BuildKit secret mounts instead of ARG or ENV.

I also follow least-privilege access, restrict permissions, rotate credentials regularly, and ensure secrets are not exposed in logs or CI/CD build output.

This approach keeps secrets separate from application images and reduces the risk of credential leakage across development, testing, and production environments.

Quick revision: Never bake secrets into images. Use runtime secret injection, a secrets manager, and BuildKit secrets for build-time credentials.