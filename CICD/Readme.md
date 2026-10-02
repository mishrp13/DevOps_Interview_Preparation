```

# 3-Tier-User-Platform-Project

1. Production CI/CD flow
Developer
   │
   │ git push
   ▼
GitHub Repository
   │
   ▼
GitHub Actions
   │
   ├── 1. Checkout Code
   │
   ├── 2. Secret Scanning
   │      └── Gitleaks
   │
   ├── 3. IaC Security
   │      ├── Checkov Terraform
   │      ├── Checkov Kubernetes
   │      └── Checkov Dockerfile
   │
   ├── 4. Dependency / Filesystem Security
   │      ├── Trivy Client
   │      └── Trivy Server
   │
   ├── 5. Code Quality
   │      ├── Client Lint
   │      └── Server Lint
   │
   ├── 6. Automated Tests
   │      ├── Client Tests
   │      └── Server Tests
   │
   ├── 7. SonarQube
   │      └── Quality Gate
   │
   ├── 8. Application Build
   │      └── Client Build
   │
   ├── 9. Docker Build
   │
   ├── 10. Container Security
   │       └── Trivy Image Scan
   │
   ├── 11. SBOM
   │       ├── Source SBOM
   │       └── Image SBOM
   │
   ├── 12. Push Image
   │       └── Docker Hub
   │
   ├── 13. Deploy
   │       └── Kubernetes
   │
   ├── 14. Deployment Verification
   │       ├── Rollout Status
   │       └── Health Check
   │
   └── 15. Rollback if Deployment Fails

Your current workflow starts on a push to the qa branch and only runs when changes occur in client, server, or the workflow itself.

2. Step-by-step interview explanation

You can explain it in simple English like this:

Step 1 — Developer pushes code

"The pipeline is triggered whenever a developer pushes code to the QA branch. I have also configured path-based triggering, so the pipeline runs when there are changes in the client, server, or CI/CD workflow."

Your workflow currently uses the qa branch and those paths.

Step 2 — Checkout source code

"The first step in each job is to checkout the source code using GitHub's checkout action. This makes the repository available on the GitHub-hosted runner."

You are using actions/checkout@v4.

Step 3 — Secret scanning with Gitleaks

"Before doing any build or deployment, I scan the repository for accidentally committed secrets such as passwords, API keys, tokens, and credentials."

Your pipeline runs Gitleaks inside Docker and generates a JSON report.

Then:

"I upload the Gitleaks report as a GitHub Actions artifact so that the security team can review it later."

Interview point:
Your current configuration uses --exit-code 0, so Gitleaks reports findings but does not fail the pipeline. That's worth knowing if the interviewer asks about enforcement.

3. Infrastructure security — Checkov

You have three Checkov jobs.

Terraform

"After secret scanning, I scan the Terraform infrastructure code using Checkov. This helps identify insecure or non-compliant Terraform configurations."

Kubernetes

"I separately scan Kubernetes manifests with Checkov to identify security and configuration issues in Kubernetes resources."

Dockerfile

"I also scan the Dockerfile using Checkov to detect container configuration issues and security misconfigurations."

All three generate reports that are uploaded as artifacts.

4. Trivy filesystem scanning

Next you scan the application source.

For the client:

"I use Trivy filesystem scanning to identify vulnerabilities in the client-side dependencies and filesystem. I focus on HIGH and CRITICAL vulnerabilities and generate both JSON and human-readable table reports."

You do the same for the server.

A good interview sentence is:

"I use Trivy at multiple stages because filesystem scanning and container image scanning solve different security problems."

That's a very good point to mention.

5. Code linting

After security scanning, you perform linting.

For the client:

"I install the Node.js dependencies using npm ci and run the client linting process."

For the server, you do the same.

Important production improvement

Currently you have:

continue-on-error: true

for linting.

So technically, lint failures will not stop the pipeline.

For a strict production pipeline, I would normally remove that unless there is a specific business reason to allow lint failures.

6. Automated testing

Next:

"After linting passes, I execute automated tests for both the client and server."

Client tests run after client-lint.

Server tests run after server-lint.

Again, your current configuration has:

continue-on-error: true

So test failures currently won't necessarily stop the pipeline.

For a true production CI/CD pipeline, I'd recommend:

continue-on-error: false

or simply removing it because false is the normal behavior.

7. SonarQube quality gate

You already have a SonarQube section, but it is commented out.

I would enable it and place it after both client and server tests.

Interview explanation:

"After automated testing, I run SonarQube analysis to check code quality, bugs, vulnerabilities, code smells, and maintainability. I then use the SonarQube quality gate to decide whether the code is acceptable for the next stage."

For production, I would make the quality gate blocking rather than continue-on-error: true.

8. Build the application

Your client build happens after the client tests.

"Once the code quality and tests are successful, I build the client application using the Node.js build process."

A production pipeline should ideally also have a server build, depending on your application architecture.

9. Build the Docker image

Then you move into containerization.

"After the application build is successful, I build the Docker image using Docker Buildx."

You currently create two tags:

mishrp/node-js-app:${{ github.sha }}
mishrp/node-js-app:latest

The important one is:

${{ github.sha }}

because it provides an immutable reference to the exact Git commit.

In an interview, say:

"I prefer deploying the SHA-based image tag because it gives me traceability. I can always identify exactly which Git commit is running in the environment."

10. Container image scanning

After building the image, you scan it with Trivy.

"I don't only scan the source code. I also scan the final Docker image because vulnerabilities can be introduced through the base image or operating-system packages."

Your image scan checks HIGH and CRITICAL vulnerabilities.

This is an important production-security concept.

11. Generate SBOM

Your pipeline generates two Software Bills of Materials.

Source SBOM

"I generate an SBOM for the source code so we have visibility into the software components and dependencies."

Image SBOM

"I also generate an SBOM for the final container image. This gives us a software inventory of what is actually packaged into the container."

Your workflow uses SPDX JSON and uploads the artifacts.

12. Push Docker image

Finally, your current Docker job pushes the image to Docker Hub.

Interview explanation:

"Once the image passes the required security checks, I push the immutable SHA-tagged image to the container registry. The registry becomes the source from which Kubernetes pulls the image."

13. Missing part — Kubernetes deployment

This is the major part I would add to your pipeline.

After Docker push:

Docker Hub
    │
    ▼
Kubernetes Deployment
    │
    ├── Update image
    ├── Rolling update
    ├── Wait for rollout
    └── Health check

For example, the deployment job conceptually should be:

deploy-qa:
  name: Deploy to QA
  needs:
    - docker

  runs-on: ubuntu-latest

  steps:
    - name: Checkout source code
      uses: actions/checkout@v4

    - name: Configure cloud credentials
      # Cloud-specific authentication

    - name: Configure kubectl
      # Configure Kubernetes access

    - name: Update Kubernetes deployment
      run: |
        kubectl set image deployment/node-js-app \
          node-js-app=mishrp/node-js-app:${{ github.sha }} \
          -n qa

    - name: Wait for rollout
      run: |
        kubectl rollout status deployment/node-js-app \
          -n qa \
          --timeout=5m

    - name: Verify deployment
      run: |
        kubectl get pods -n qa
        kubectl get deployment node-js-app -n qa

The exact authentication depends on whether you are using AWS EKS, Azure AKS, GCP GKE, or another Kubernetes platform, so I would not hard-code cloud-specific authentication without knowing your environment.

14. Health check

A production pipeline should not stop at:

kubectl rollout status

You should also verify that the application is actually responding.

For example:

Deployment
    ↓
Pods Ready?
    ↓
Service available?
    ↓
Application health endpoint?
    ↓
Success

Interview explanation:

"After Kubernetes reports a successful rollout, I perform an application-level health check. This is important because a pod can be running while the application itself is unhealthy."

15. Rollback

This is another important production feature.

If the deployment fails:

kubectl rollout undo deployment/node-js-app -n qa

Then:

kubectl rollout status deployment/node-js-app -n qa

Interview explanation:

"If the new version fails the rollout or health checks, I roll back to the previous known-good ReplicaSet. This reduces deployment risk and helps maintain application availability."

16. One important improvement: don't deploy latest

Your current pipeline creates:

mishrp/node-js-app:latest
mishrp/node-js-app:${github.sha}

For production deployment, I recommend:

mishrp/node-js-app:${github.sha}

and Kubernetes should deploy the SHA tag, not latest.

Why?

Because:

latest
   ↓
changes over time
   ↓
harder to identify exact version

Whereas:

abc123456
   ↓
immutable reference
   ↓
Git commit
   ↓
easy rollback
17. Your final production architecture

I would present your pipeline to an interviewer as:

                   Developer
                       │
                       ▼
                GitHub Repository
                       │
                    Push QA
                       │
                       ▼
              ┌─────────────────┐
              │ GitHub Actions  │
              └────────┬────────┘
                       │
             ┌─────────▼─────────┐
             │   Gitleaks Scan   │
             └─────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Checkov      Checkov      Checkov
      Terraform     K8s        Dockerfile
          │            │            │
          └────────────┼────────────┘
                       ▼
                Trivy FS Scan
                       │
                       ▼
                 Linting
                 /     \
                ▼       ▼
           Client Test  Server Test
                \       /
                 \     /
                   ▼
               SonarQube
             Quality Gate
                   │
                   ▼
              Application
                 Build
                   │
                   ▼
              Docker Build
                   │
                   ▼
             Trivy Image Scan
                   │
                   ▼
              Generate SBOM
                   │
                   ▼
              Docker Registry
                   │
                   ▼
            Kubernetes Cluster
                   │
             Rolling Update
                   │
                   ▼
             Rollout Status
                   │
                   ▼
              Health Check
                   │
             ┌─────┴─────┐
             │           │
           Success      Failure
             │           │
             ▼           ▼
          Complete     Rollback
The 60-second interview answer

If the interviewer says "Explain your CI/CD pipeline", don't explain every YAML line. Say this:

My CI/CD pipeline is implemented using GitHub Actions and follows a security-first production workflow.
Whenever a developer pushes code to the QA branch, the pipeline is triggered for changes in the client, server, or workflow files.
First, I checkout the source code and run Gitleaks to detect accidentally committed secrets.
Next, I perform infrastructure security scanning using Checkov for Terraform, Kubernetes manifests, and Dockerfiles.
Then I use Trivy filesystem scanning to identify HIGH and CRITICAL vulnerabilities in the application dependencies.
After the security checks, I run linting and automated tests for both the client and server applications. I also integrate SonarQube for static code analysis and quality-gate validation.
Once the code quality and tests are successful, I build the application and create a Docker image using Docker Buildx then I tag the image with the Git commit SHA so that every deployment is traceable to a specific source-code version.Before pushing the image to the container registry, I scan the final Docker image with Trivy. I also generate SBOMs for both the source code and container image for software-component visibility.After all required checks pass, the image is pushed to the container registry.
The next stage is deployment to Kubernetes. I update the Kubernetes deployment with the SHA-tagged image, perform a rolling update, wait for the rollout to complete, and perform an application health check.
If the deployment or health check fails, I roll back to the previous stable version.

So overall, the pipeline provides automated CI, security scanning, code-quality validation, container security, SBOM generation, artifact management, Kubernetes deployment, health verification, and rollback capability.



-------------------------------------------------------------------------------

Exactly. In an interview, don't try to reproduce your entire 850-line pipeline from memory. The interviewer is usually testing whether you understand the flow, dependencies, security gates, and deployment, not whether you memorized YAML.

Based on your pipeline, I would memorize a clean production-style template like this.

1. Start with the basic skeleton

Write this first:

name: Enterprise CI/CD Pipeline

on:
  push:
    branches:
      - qa

permissions:
  contents: read
  id-token: write

jobs:

Then explain:

"I am triggering the pipeline when code is pushed to the QA branch. I use least-privilege permissions and OIDC for cloud authentication."

2. Write security scanning first
Gitleaks
  gitleaks:
    name: Gitleaks Secret Scan
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2

Interview explanation:

"My first security gate is secret scanning. I use Gitleaks to make sure developers have not committed passwords, tokens, API keys, or other secrets."

3. Add Checkov

You don't need to write three huge jobs during an interview. Show that you understand what you're scanning.

  checkov:
    name: IaC Security Scan
    runs-on: ubuntu-latest
    needs: gitleaks

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Checkov
        run: pip install checkov

      - name: Scan Terraform
        run: checkov -d . --framework terraform

      - name: Scan Kubernetes
        run: checkov -d . --framework kubernetes

      - name: Scan Dockerfile
        run: checkov -d . --framework dockerfile

Say:

"Next I scan Terraform, Kubernetes manifests, and Dockerfiles with Checkov to identify infrastructure and container configuration issues."

4. Add Trivy filesystem scan
  trivy-fs:
    name: Trivy Filesystem Scan
    runs-on: ubuntu-latest
    needs: gitleaks

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Trivy
        uses: aquasecurity/setup-trivy@v0.2.6

      - name: Scan application
        run: |
          trivy fs . \
            --severity HIGH,CRITICAL \
            --ignore-unfixed \
            --exit-code 1

Notice the difference from your current pipeline:

--exit-code 1

means the pipeline can fail when vulnerabilities are found.

You can explain:

"I use Trivy to scan application dependencies and filesystem vulnerabilities. For production, I configure the security threshold so critical findings can block the pipeline."

5. Add lint and tests

Now write client/server quality checks.

  client-test:
    name: Client Lint and Test
    runs-on: ubuntu-latest
    needs:
      - checkov
      - trivy-fs

    defaults:
      run:
        working-directory: client

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm
          cache-dependency-path: client/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

And similarly:

  server-test:
    name: Server Lint and Test
    runs-on: ubuntu-latest
    needs:
      - checkov
      - trivy-fs

    defaults:
      run:
        working-directory: server

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm
          cache-dependency-path: server/package-lock.json

      - run: npm ci
      - run: npm run lint
      - run: npm test

Interview explanation:

"After security checks, I install dependencies with npm ci, run linting, and execute automated tests for both frontend and backend."

6. SonarQube

Then:

  sonarqube:
    name: SonarQube Analysis
    runs-on: ubuntu-latest
    needs:
      - client-test
      - server-test

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v6
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

Say:

"Once tests pass, I perform static code analysis with SonarQube. The quality gate determines whether the code is good enough to proceed."

7. Build the application

For example:

  build:
    name: Application Build
    runs-on: ubuntu-latest
    needs: sonarqube

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Build Client
        working-directory: client
        run: |
          npm ci
          npm run build

Say:

"After the quality gate passes, I build the application."

8. Docker build

This is an important part to remember:

  docker:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Setup Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build Image
        uses: docker/build-push-action@v7
        with:
          context: .
          push: false
          load: true
          tags: |
            myapp:${{ github.sha }}

The key thing to remember:

github.sha

Interview line:

"I tag the image with the Git commit SHA instead of relying only on latest because it gives me immutable versioning and traceability."

9. Scan the Docker image

Then:

      - name: Trivy Image Scan
        run: |
          trivy image \
            --severity HIGH,CRITICAL \
            --ignore-unfixed \
            --exit-code 1 \
            myapp:${{ github.sha }}

Explain:

"After creating the image, I scan the actual container image. This is important because vulnerabilities can exist in the base image and OS packages even when the application source code is clean."

10. Generate SBOM

You can write:

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          image: myapp:${{ github.sha }}
          format: spdx-json
          output-file: sbom.spdx.json

Say:

"I generate an SBOM so that I have an inventory of the software components inside the container."

11. Push the image

After all security checks:

      - name: Push Docker Image
        uses: docker/build-push-action@v7
        with:
          context: .
          push: true
          tags: |
            myregistry/myapp:${{ github.sha }}

Interview explanation:

"Only after the required security and quality gates pass do I push the image to the container registry."

12. Kubernetes deployment

This is the part your current uploaded pipeline doesn't yet contain, but you should add it when asked to write a complete production pipeline.

  deploy:
    name: Deploy to Kubernetes
    runs-on: ubuntu-latest
    needs: docker

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure Kubernetes
        run: |
          # Configure cloud credentials
          # Configure kubectl

      - name: Deploy
        run: |
          kubectl set image deployment/myapp \
            myapp=myregistry/myapp:${{ github.sha }} \
            -n qa

      - name: Verify rollout
        run: |
          kubectl rollout status deployment/myapp \
            -n qa \
            --timeout=5m

Explain:

"After the image is pushed, I deploy the exact SHA-tagged image to Kubernetes. Kubernetes performs a rolling update, and I wait for the rollout to complete."

13. Health check + rollback

This makes your answer sound production-level:

      - name: Health Check
        run: |
          kubectl get pods -n qa
          kubectl get deployment myapp -n qa

      - name: Rollback
        if: failure()
        run: |
          kubectl rollout undo deployment/myapp -n qa

Then tell the interviewer:

"If the rollout or health check fails, I rollback to the previous stable version."

The order you should memorize

Don't memorize 500 lines.

Memorize this:

1. Trigger
      ↓
2. Checkout
      ↓
3. Gitleaks
      ↓
4. Checkov
      ↓
5. Trivy FS
      ↓
6. Lint
      ↓
7. Unit Tests
      ↓
8. SonarQube
      ↓
9. Build Application
      ↓
10. Docker Build
      ↓
11. Trivy Image Scan
      ↓
12. SBOM
      ↓
13. Push Registry
      ↓
14. Kubernetes Deploy
      ↓
15. Rollout Verification
      ↓
16. Health Check
      ↓
17. Rollback on Failure
And memorize the dependency chain

This is even more important:

gitleaks
   ↓
checkov + trivy-fs
   ↓
lint + tests
   ↓
sonarqube
   ↓
build
   ↓
docker build
   ↓
trivy image
   ↓
sbom
   ↓
push
   ↓
deploy
   ↓
verify

Your existing pipeline follows essentially this security → quality → build → containerization flow, although some of your current scans/tests are configured as non-blocking and the deployment stage is not yet present.

⭐ What I would actually write on the interview whiteboard

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

```