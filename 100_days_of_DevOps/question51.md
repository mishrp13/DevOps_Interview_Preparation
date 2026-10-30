```
An application currently running on the Kubernetes cluster employs the nginx web server. The Nautilus application development team has introduced some recent changes that need deployment. They've crafted an image nginx:1.19 with the latest updates.


Execute a rolling update for this application, integrating the nginx:1.19 image. The deployment is named nginx-deployment.

Ensure all pods are operational post-update.

Note: The kubectl utility on the jump-host has been configured to work with the Kubernetes cluster.

sol:

kubectl set image deployment/nginx-deployment nginx-container=nginx:1.19

kubectl rollout status deployment/nginx-deployment