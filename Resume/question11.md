```
•	Implemented Docker security hardening practices to improve container security and reduce image vulnerabilities.

“I worked on hardening Docker images and containers to improve security and reduce vulnerabilities. First, we reviewed our Dockerfiles and container images to identify security risks.
We used trusted base images and kept them updated, scanned images for known vulnerabilities, and removed unnecessary packages to reduce the attack surface. We also ensured containers ran as non-root users instead of using the root user wherever possible.
Additionally, we avoided storing passwords, tokens, or other sensitive information directly in Dockerfiles. We configured appropriate container permissions and integrated image security checks into the CI/CD pipeline so that vulnerable images could be identified before deployment.
These practices helped improve image security and reduce the risk of running vulnerable containers in our Kubernetes environment.”