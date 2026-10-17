```
DNS, networking, load balancers, and firewalls
Resume point: Configured DNS, firewall rules, load balancers, and application infrastructure.
Question: Explain how external traffic reaches an application running in EKS.

When external traffic reaches an application running in Amazon EKS, the request typically passes through DNS, a load balancer, network security controls, and Kubernetes routing before reaching the application pod.

First, the user accesses the application using a domain name, such as `app.example.com`. Amazon Route 53 resolves the domain to the AWS load balancer's DNS name.

Next, the request reaches an Application Load Balancer in public subnets. The ALB listener accepts HTTPS traffic on port 443, and TLS can be terminated at the load balancer using an ACM certificate. Listener rules can route requests based on the hostname or URL path.

The AWS Load Balancer Controller in EKS manages the ALB configuration based on Kubernetes Ingress resources. The ALB forwards traffic to a target group containing either pod IPs or worker-node targets, depending on the configuration.

Security groups control permitted inbound and outbound traffic, while subnet route tables and network ACLs also affect connectivity. Kubernetes network policies may further restrict pod-to-pod or ingress traffic if a supporting network implementation is configured.

Finally, the request reaches the application container listening on the configured port. The response travels back through the established network path.

I would also configure health checks and monitoring so that unhealthy targets are removed from service and connectivity problems can be diagnosed quickly.