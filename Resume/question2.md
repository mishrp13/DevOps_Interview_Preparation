```
Amazon EKS and Kubernetes
Resume point: Built and managed Kubernetes environments, including Amazon EKS.
Question: Explain the architecture of your EKS cluster and how you manage it.
Be prepared to explain:
- EKS control plane versus worker nodes.
- Managed node groups and how pods are scheduled.
- How applications communicate inside and outside the cluster.
- How you upgrade the cluster and worker nodes safely.
- How you troubleshoot a pod stuck in Pending, CrashLoopBackOff, or ImagePullBackOff.
Likely follow-up: A pod is running, but the application is inaccessible. How would you troubleshoot it?


In my project, I worked with Amazon EKS to run containerized applications on Kubernetes. The architecture consisted of the EKS control plane, worker nodes, application pods, Kubernetes networking, and the components required to expose and monitor applications.

The EKS control plane is managed by AWS. It includes the Kubernetes API server and other control-plane components responsible for maintaining the desired cluster state and coordinating scheduling.

The worker nodes run in our AWS VPC and provide the compute capacity for application pods. We can use EKS managed node groups to manage the EC2 worker instances and integrate node lifecycle operations with EKS.

For application deployment, we use Kubernetes resources such as Deployments, Services, ConfigMaps, Secrets, and Ingress or other load-balancing resources, depending on the application requirements.

For external access, an AWS load balancer can route traffic to the application through Kubernetes networking. For internal communication, applications use Kubernetes Services and cluster DNS.

For day-to-day management, I focus on deployments, scaling, monitoring, troubleshooting pod failures, and maintaining compatibility between the Kubernetes version, worker nodes, and cluster add-ons. I also follow a controlled upgrade process to reduce application downtime.

