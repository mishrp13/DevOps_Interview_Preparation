```
Helm charts and Kubernetes manifests
Resume point: Developed and maintained Helm charts and Kubernetes manifests for microservices.
Question: Why did you use Helm instead of maintaining only plain Kubernetes YAML files?
Prepare to explain:
- Charts, templates, values.yaml, and releases.
- How you maintained different values for development, staging, and production.
- How you upgraded and rolled back a release.
- How you managed configuration and sensitive values.
- The difference between helm install, helm upgrade, and helm rollback.
Likely follow-up: A Helm upgrade fails halfway through. How would you investigate and recover?


In my project, we used Helm to manage Kubernetes deployments for multiple microservices.

Maintaining separate Kubernetes YAML files for every environment would have created duplication and made it harder to keep configurations consistent. Helm helped us create reusable charts with templates and configurable values.

We defined common Kubernetes resources, such as Deployments, Services, ConfigMaps, and Ingress resources, in Helm templates. Environment-specific settings, such as replica counts, image tags, resource requests and limits, and application configuration, were provided through values files.

For example, development could use fewer replicas and smaller resource allocations, while production could use higher availability settings and production-specific configuration.

We used Helm releases to track deployments and manage upgrades. When deploying a new application version, we could upgrade the existing release with updated values. If the upgrade caused problems, we could inspect the release history and roll back to a previous revision when appropriate.

Overall, Helm reduced YAML duplication, improved consistency across environments, and made application deployment and release management easier to maintain.