```
Prometheus and Grafana monitoring
Resume point: Implemented monitoring and alerting for Kubernetes and application workloads.
Question: How did you configure Prometheus and Grafana to monitor your EKS cluster?
Prepare to explain:
- How Prometheus collects metrics and how Grafana visualizes them.
- Which metrics you monitored: CPU, memory, pod restarts, node health, latency, and error rates.
- How you configured dashboards and alert rules.
- How you routed alerts to the appropriate team or notification channel.
- How you distinguished a Kubernetes infrastructure issue from an application issue.
Likely follow-up: CPU utilization suddenly reaches 90% across multiple pods. How would you investigate?


In my project, we used Prometheus and Grafana to monitor Kubernetes infrastructure and application workloads running on Amazon EKS.

Prometheus collected metrics from configured targets, including node-level exporters, Kubernetes metrics endpoints, and application endpoints where instrumentation was available. We used these metrics to understand CPU and memory utilization, pod health, restarts, node capacity, and application performance.

We used Grafana to connect to Prometheus as a data source and create dashboards for cluster health, node resource utilization, pod status, and application metrics.

For alerting, we defined thresholds and conditions for issues such as high CPU or memory usage, repeated pod restarts, unavailable replicas, and application errors. Depending on the alerting setup, notifications were routed through Alertmanager or Grafana-managed alerting to the appropriate team or notification channel.

During troubleshooting, we correlated infrastructure metrics with application metrics and logs. For example, if CPU usage increased across multiple pods, we checked whether the issue was caused by increased traffic, inefficient application processing, resource limits, or insufficient node capacity.

This monitoring setup helped us detect issues earlier, investigate incidents faster, and understand the health of both the Kubernetes environment and the applications running on it.