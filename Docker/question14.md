```
•How do you scan images for vulnerabilities? (Trivy, ECR scanning)

In a DevOps interview, Docker image vulnerability scanning means checking container images for known security weaknesses before deploying them to production.

Tools such as Trivy and Amazon ECR image scanning help identify vulnerabilities in operating-system packages, application dependencies, and other components included in an image.

The main goal is to detect security issues early in the CI/CD pipeline and prevent vulnerable images from reaching production.

1. What vulnerabilities do we scan for?

When you scan a Docker image, the scanner can identify:

OS package vulnerabilities: Vulnerable packages in Alpine, Debian, Ubuntu, and other base images.

Application dependency vulnerabilities: Known CVEs in libraries such as Python packages, npm modules, or Java dependencies.

Severity levels: Critical, High, Medium, and Low.

Misconfigurations and exposed secrets: Depending on the scanner and enabled scanning options.

A CVE (Common Vulnerabilities and Exposures) is an identifier for a publicly documented security vulnerability.

2. Method 1: Scan Docker images using Trivy

Trivy is an open-source security scanner commonly used in DevOps pipelines to scan container images, dependencies, filesystems, and configuration files.

Typical use: Local development, Jenkins, GitHub Actions, GitLab CI, and other CI/CD pipelines.

Step 1: Build your Docker image
docker build -t myapp:latest .
Step 2: Scan the image
trivy image myapp:latest

Trivy reports vulnerabilities found in the image, including their severity, affected package, and available fixes when known.

Step 3: Fail the build for critical or high vulnerabilities
trivy image \
  --severity HIGH,CRITICAL \
  --exit-code 1 \
  myapp:latest

This command returns a non-zero exit code when matching High or Critical vulnerabilities are detected, allowing the CI/CD pipeline to fail.

Step 4: Generate a report
trivy image \
  --format json \
  --output trivy-report.json \
  myapp:latest

You can archive the report as a CI/CD artifact for security review and auditing.

3. Method 2: Scan images using Amazon ECR

Amazon Elastic Container Registry (ECR) is AWS's managed container image registry. It can scan images for known software vulnerabilities.

1. Build Docker image

CI/CD pipeline creates the image.

2. Push image to Amazon ECR

Image is stored in a private or public repository.

3. ECR scans the image

Basic or enhanced scanning detects known vulnerabilities.

4. Review findings and enforce policy


Example AWS CLI workflow

Step 1: Push the image to ECR

After authenticating Docker to your ECR registry and tagging the image:

docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myapp:latest

Step 2: Start a manual scan, if supported by your repository's scanning configuration

aws ecr start-image-scan \
  --repository-name myapp \
  --image-id imageTag=latest

Step 3: Retrieve scan findings

aws ecr describe-image-scan-findings \
  --repository-name myapp \
  --image-id imageTag=latest

These commands assume your AWS CLI is configured with suitable permissions and the repository's scanning configuration supports the requested operation. Enhanced scanning findings are generally accessed through Amazon Inspector.

Interview tip: Scanning identifies vulnerabilities, but a secure pipeline must also decide whether an image is allowed to proceed to deployment.

4. How do you integrate vulnerability scanning into CI/CD?

For example, in a Jenkins pipeline:

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t myapp:$BUILD_NUMBER .'
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                  trivy image \
                    --severity HIGH,CRITICAL \
                    --exit-code 1 \
                    myapp:$BUILD_NUMBER
                '''
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker push myapp:$BUILD_NUMBER'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy only approved images'
            }
        }
    }
}

In this example, if Trivy detects a High or Critical vulnerability, the scan step fails and Jenkins stops the pipeline before the push or deployment stages.

For this to work as intended, the pipeline agent must have Trivy installed and Docker registry authentication configured. In production, use an approved image tag and immutable digest rather than relying on latest.

A real deployment pipeline should also:

Decide how to handle vulnerabilities without available fixes.

Allow documented exceptions with approval and expiry dates.

Store scan reports for auditing.

Rescan images as new CVEs are disclosed.

Scan the exact image digest that will be deployed.

5. Common DevOps interview questions

Q1. What is the difference between Trivy and ECR scanning?

Trivy is a flexible scanner that can be integrated into many CI/CD platforms and used locally. ECR scanning is integrated with AWS's image registry and can use AWS-native scanning or Amazon Inspector for enhanced scanning and ongoing monitoring.

Q2. What happens if a Critical vulnerability is found?

I would check the affected package, CVE, severity, and whether a patched version is available. Then I would update the base image or dependency, rebuild the image, scan it again, and block production deployment until the issue is resolved or an authorized exception is granted.

Q3. Should we scan only once when building the image?

No. I would scan during CI/CD and enable ongoing scanning where available. A previously clean image can become vulnerable when new CVEs are disclosed.

Q4. Does a successful vulnerability scan guarantee a secure image?

No. Scanners primarily detect known vulnerabilities and other supported issues. They cannot guarantee that an image is free from every vulnerability, malware, misconfiguration, or application-level security flaw.

6. Interview answer to memorize
Writing

In DevOps, I integrate container image vulnerability scanning into the CI/CD pipeline to identify security issues before deployment.

I commonly use Trivy to scan Docker images for operating-system and application dependency vulnerabilities. I configure the scan to fail the pipeline when vulnerabilities exceed the defined severity threshold, such as High or Critical.

In AWS environments, I can also use Amazon ECR image scanning, including enhanced scanning with Amazon Inspector, to detect vulnerabilities and monitor images over time.

If vulnerabilities are found, I review the CVEs, update the affected packages or base image, rebuild the image, and scan it again. I also retain scan reports and use approved exceptions when an issue cannot be fixed immediately.

This approach helps prevent vulnerable container images from reaching production and improves security across the CI/CD lifecycle.

Quick revision: Build image → Scan with Trivy or ECR → Enforce severity policy → Fix vulnerabilities → Rescan → Deploy the approved image.