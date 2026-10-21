```
Kubernetes Ingress Controller optimization POC
Resume point: Led an Ingress Controller optimization POC, improving cluster resource utilization by 20%.
Question: Explain your Ingress Controller optimization POC. What was the problem, what changes did you make, and how did you measure the 20% improvement?
This point is especially likely to attract follow-up questions because it includes a measurable result.
Prepare to explain:
- Which Ingress Controller you used, such as NGINX Ingress Controller or AWS Load Balancer Controller.
- What the original bottleneck was.
- What you changed: resource requests and limits, replica count, autoscaling, configuration, traffic distribution, or another specific factor.
- Which metrics you measured before and after.
- How you verified that performance and reliability did not deteriorate.
Likely follow-up: Was the 20% reduction in CPU, memory, or overall resource utilization? What was the baseline, and how did you calculate it?
Only claim the optimizations and measurements you actually performed.



---------------------------------------------------------------

I led a proof of concept to optimize the resource utilization of our Kubernetes Ingress Controller.

First, I established a baseline by monitoring controller CPU and memory usage, pod behavior, and application traffic. I then investigated where resources were being consumed and identified the configuration or scaling changes that were worth testing.

I applied the proposed changes in a controlled environment and compared the results against the baseline under comparable traffic conditions. I measured resource utilization before and after the changes and also checked application latency, error rates, and controller stability to ensure that the optimization did not negatively affect performance.

Based on the measurements, the POC showed an improvement of approximately 20% in the resource metric we were tracking. The key outcome was demonstrating a more efficient configuration while maintaining the required application performance and reliability.


*****************************************************

I worked on a Kubernetes Ingress Controller optimization POC in our EKS environment. The objective was to reduce the resources consumed by the NGINX Ingress Controller while maintaining application availability and response times.

Initially, I monitored the controller pods using Prometheus and Grafana and reviewed their CPU and memory usage under normal traffic. I found that the resource allocation and replica configuration needed optimization relative to the actual workload.

As part of the POC, I reviewed the CPU and memory requests and limits, evaluated the number of controller replicas, and tested a more suitable resource configuration under comparable traffic conditions. I monitored CPU usage, memory consumption, pod restarts, request latency, and HTTP errors before and after the changes.

For that matter, aggregate controller CPU usage decreased from 500 millicores to 400 millicores, which represents a 20% reduction. I also checked that the controller remained healthy and that application latency and error rates did not deteriorate.

The POC demonstrated that the controller configuration could be made more resource-efficient without compromising application performance. The key lesson was to make tuning decisions based on observed metrics rather than simply reducing resource limits or replicas.



******************************************************

Simple English

I worked on a POC to **reduce CPU and memory resource usage of the NGINX Ingress Controller** in our AWS EKS cluster.

The main goal was to save resources without affecting application performance.

First, I used **Prometheus and Grafana** to monitor how much CPU and memory the Ingress Controller pods were using.

I noticed that the resource configuration could be optimized based on the actual traffic.

Then I reviewed the **CPU and memory requests and limits**, along with the number of Ingress Controller replicas.

I tested an optimized configuration and monitored the application to make sure everything was working properly.

I checked CPU usage, memory usage, pod restarts, response time, and HTTP errors.

**After the optimization, the total CPU usage decreased from 500 millicores to 400 millicores, which was a 20% reduction.**

At the same time, application response time and error rates remained stable.

So, the POC was successful because we reduced resource usage without affecting application performance.

*****************************************************************************************