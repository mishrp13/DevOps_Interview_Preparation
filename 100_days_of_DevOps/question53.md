```

We encountered an issue with our Nginx and PHP-FPM setup on the Kubernetes cluster this morning, which halted its functionality. Investigate and rectify the issue:



The pod name is nginx-phpfpm and configmap name is nginx-config. Identify and fix the problem.


Once resolved, copy /home/thor/index.php file from the jump host to the nginx-container within the nginx document root. After this, you should be able to access the website using Website button on the top bar.


Note: The kubectl utility on the jump-host has been configured to work with the Kubernetes cluster.

sol:
Recently, I worked on troubleshooting a Nginx and PHP-FPM application running inside a Kubernetes Pod.

The Pod contained two containers: an Nginx container and a PHP-FPM container. Both containers shared an EmptyDir volume to access the application files.

Initially, I checked the Kubernetes resources using `kubectl get all -o wide`. The Pod and both containers were running, so I moved on to checking the application configuration.

I inspected the Nginx ConfigMap using `kubectl describe configmap nginx-config` and then examined the Pod YAML using:

`kubectl get pod nginx-phpfpm -o yaml`

While checking the volume mounts, I noticed that the Nginx container was mounting the shared volume at `/usr/share/nginx/html`, whereas the PHP-FPM container was mounting the same volume at `/var/www/html`.

This path mismatch was causing the application files to be accessed through inconsistent document-root paths.

To fix the issue, I exported the Pod YAML, updated the Nginx container's volume mount path to `/var/www/html`, and recreated the standalone Pod using:

`kubectl replace -f /tmp/nginx.yaml --force`

After the Pod was recreated, I copied the index.php file from the jump host into the shared volume using `kubectl cp`.

Finally, I validated the application using curl on port 8099 and received an HTTP 200 OK response.

This confirmed that the application was working again and that Nginx could successfully communicate with PHP-FPM.