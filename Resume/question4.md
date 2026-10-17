```
Resume point: Built and pushed Docker images to ECR and deployed applications to EKS.
Question: Explain the complete workflow from building a Docker image to running it in EKS.
A strong answer should cover:
1. Code is committed to the repository.
2. The pipeline builds and tests the application.
3. Docker builds an image tagged with a version or commit SHA.
4. The image is pushed to Amazon ECR.
5. Kubernetes manifests or Helm charts reference that image.
6. The pipeline deploys to EKS and verifies rollout health.
Likely follow-up: What would you check if EKS reports ImagePullBackOff when pulling an image from ECR?

In my project, I used Docker, Amazon ECR, and Amazon EKS as part of the application deployment workflow.

First, developers committed the application code to the source repository. This triggered the CI/CD pipeline, which checked out the code and ran the required build, unit tests, and validation steps.

Next, we built a Docker image using the application's Dockerfile. We tagged the image with a version or Git commit SHA so that each deployment could be associated with a specific code revision.

After building the image, the pipeline authenticated to Amazon ECR, tagged the image with the ECR repository URI, and pushed it to the repository.

The deployment configuration used that image URI. Depending on the project, we updated Kubernetes YAML manifests or Helm chart values to reference the new image.

The pipeline then connected to the appropriate EKS cluster, configured Kubernetes access, and deployed the updated application using `kubectl apply` or Helm.

Kubernetes created or updated the Deployment. The scheduler placed the pods on eligible worker nodes, and the container runtime on each node pulled the image from ECR and started the containers.

Finally, I verified the deployment using commands such as `kubectl rollout status`, `kubectl get pods`, and `kubectl logs`. I also checked readiness probes and application health to confirm that the new version was running correctly.

If the deployment failed, I would inspect the pod events, logs, image reference, IAM permissions, and networking to identify the root cause before proceeding.