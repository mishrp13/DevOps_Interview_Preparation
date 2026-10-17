```

Resume point: Implemented Blue-Green and Canary deployment approaches.
Question: Explain the difference between Blue-Green and Canary deployments. How did you implement them, and how would you roll back a bad release?

I implemented Blue-Green and Canary deployment approaches to reduce the risk of releasing new application versions.

In Blue-Green deployment, we maintain the current version and a separate environment running the new version. We validate the new version using health checks and smoke tests, and then switch production traffic to it. If an issue occurs, we can route traffic back to the previous version, provided it remains healthy and compatible.

In Canary deployment, we release the new version to a small percentage of traffic first. We monitor application health, error rates, and response latency, then gradually increase traffic if the metrics remain healthy. If the canary causes problems, we stop the rollout and direct traffic back to the stable version.

In Kubernetes, these approaches can be implemented using separate Deployments and Services, together with Ingress traffic management or a progressive delivery tool. The key difference is that Blue-Green uses a traffic switch between environments, while Canary validates the new release incrementally with real traffic.

For rollback, I would stop the rollout, restore traffic to the known-good version, verify application health, and investigate the failure before retrying the release.