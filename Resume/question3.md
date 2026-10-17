```
Resume point: Built CI/CD pipelines to automate build, testing, and deployment.
Question: Walk me through a CI/CD pipeline you built, from code commit to production deployment.
Be prepared to explain:
- What triggers the pipeline.
- How code is checked out, built, and tested.
- How artifacts or Docker images are versioned.
- How credentials and secrets are managed.
- How approvals, failed builds, rollbacks, and notifications are handled.
Likely follow-up: What happens if the build succeeds but the deployment fails?


My CI/CD pipeline is implemented using GitHub Actions and follows a security-first production workflow.
Whenever a developer pushes code to the QA branch, the pipeline is triggered for changes in the client, server, or workflow files.
First, I checkout the source code and run Gitleaks to detect accidentally committed secrets.
Next, I perform infrastructure security scanning using Checkov for Terraform, Kubernetes manifests, and Dockerfiles.
Then I use Trivy filesystem scanning to identify HIGH and CRITICAL vulnerabilities in the application dependencies.
After the security checks, I run linting and automated tests for both the client and server applications. I also integrate SonarQube for static code analysis and quality-gate validation.
Once the code quality and tests are successful, I build the application and create a Docker image using Docker Buildx then I tag the image with the Git commit SHA so that every deployment is traceable to a specific source-code version.Before pushing the image to the container registry, I scan the final Docker image with Trivy. I also generate SBOMs for both the source code and container image for software-component visibility.After all required checks pass, the image is pushed to the container registry.
The next stage is deployment to Kubernetes. I update the Kubernetes deployment with the SHA-tagged image, perform a rolling update, wait for the rollout to complete, and perform an application health check.
If the deployment or health check fails, I roll back to the previous stable version.



What I would actually write on the interview whiteboard

If they give you only 10–15 minutes, write:

name: CI-CD

on:
  push:
    branches: [qa]

permissions:
  contents: read
  id-token: write

jobs:

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: gitleaks detect
      - run: checkov -d .
      - run: trivy fs . --severity HIGH,CRITICAL

  test:
    needs: security
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint
      - run: npm test

  quality:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: SonarSource/sonarqube-scan-action@v6

  docker:
    needs: quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v4
      - uses: docker/setup-buildx-action@v4

      - name: Build image
        uses: docker/build-push-action@v7
        with:
          push: false
          load: true
          tags: myapp:${{ github.sha }}

      - name: Scan image
        run: trivy image myapp:${{ github.sha }}

      - name: Generate SBOM
        uses: anchore/sbom-action@v0

      - name: Push image
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: myregistry/myapp:${{ github.sha }}

  deploy:
    needs: docker
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/myapp \
            myapp=myregistry/myapp:${{ github.sha }}

      - name: Verify
        run: |
          kubectl rollout status deployment/myapp

      - name: Rollback
        if: failure()
        run: |
          kubectl rollout undo deployment/myapp

This is the version I'd memorize. If the interviewer asks for more detail, expand each job rather than trying to remember your entire real-world YAML.