```

We encountered an issue with our Nginx and PHP-FPM setup on the Kubernetes cluster this morning, which halted its functionality. Investigate and rectify the issue:



The pod name is nginx-phpfpm and configmap name is nginx-config. Identify and fix the problem.


Once resolved, copy /home/thor/index.php file from the jump host to the nginx-container within the nginx document root. After this, you should be able to access the website using Website button on the top bar.


Note: The kubectl utility on the jump-host has been configured to work with the Kubernetes cluster.

sol:

1. Check the pod and ConfigMap
kubectl get pods
kubectl describe pod nginx-phpfpm
kubectl get configmap nginx-config -o yaml


2. Edit the ConfigMap
kubectl edit configmap nginx-config


In nginx.conf, ensure these directives are configured correctly:
root /usr/share/nginx/html;
index index.html index.htm index.php;

location ~ \.php$ {
    include fastcgi_params;
    fastcgi_param REQUEST_METHOD $request_method;
    fastcgi_param SCRIPT_FILENAME /var/www/html$fastcgi_script_name;
    fastcgi_pass 127.0.0.1:9000;
}


Keep the existing events, http, server, and other configuration blocks. Save and exit.
3. Test and reload Nginx
kubectl exec nginx-phpfpm -c nginx-container -- nginx -t


If the test succeeds:
kubectl exec nginx-phpfpm -c nginx-container -- nginx -s reload


4. Copy index.php from the jump host
kubectl cp /home/thor/index.php nginx-phpfpm:/usr/share/nginx/html/index.php -c nginx-container


5. Verify the PHP file
kubectl exec nginx-phpfpm -c nginx-container -- ls -l /usr/share/nginx/html/index.php
kubectl exec nginx-phpfpm -c php-fpm-container -- ls -l /var/www/html/index.php


Both paths should show the file because the containers share the same volume.
6. Verify pod health and logs
kubectl get pod nginx-phpfpm
kubectl logs nginx-phpfpm -c nginx-container --tail=50
kubectl logs nginx-phpfpm -c php-fpm-container --tail=50


The pod should show 2/2 Running.

Finally, click the Website button in the top bar to verify that the application works.


summary

Summary: Nginx and PHP-FPM Kubernetes Fix
Issue: The Nginx and PHP-FPM pod was running, but the website was not functioning correctly because the Nginx document root was configured incorrectly.
What was wrong?
- Nginx container: The shared volume was mounted at /usr/share/nginx/html.
- PHP-FPM container: The same shared volume was mounted at /var/www/html.
- Nginx configuration: The document root was set to /var/www/html, which was not the correct path inside the Nginx container.
How we fixed it
1. Updated the ConfigMap nginx-config to set the Nginx document root to /usr/share/nginx/html.
2. Corrected the PHP script path so PHP-FPM resolves scripts under /var/www/html:
   fastcgi_param SCRIPT_FILENAME /var/www/html$fastcgi_script_name;
3. Validated and reloaded Nginx using nginx -t and nginx -s reload.
4. Copied index.php from the jump host into the Nginx document root:
   kubectl cp /home/thor/index.php nginx-phpfpm:/usr/share/nginx/html/index.php -c nginx-container
Final result
The configuration was corrected to respect the different mount paths in each container, and the PHP file was placed in the shared volume so both containers could access it.

Verification: Confirm that Nginx reload succeeded, the PHP file exists at /var/www/html/index.php inside PHP-FPM, and the website loads using the Website button.


--------------------------------------------------------------------------------------

“In this task, I was troubleshooting a web application running on Kubernetes that used Nginx as a web server and PHP-FPM to execute PHP scripts.

The application ran inside a single pod named nginx-phpfpm, which contained two containers: nginx-container and php-fpm-container.

First, I checked the pod status using kubectl get pods and kubectl describe pod. Both containers were running, so the problem wasn't that the containers had crashed.

Next, I inspected the nginx-config ConfigMap and found a mismatch in the document root configuration. Nginx was configured to serve files from /var/www/html, but the shared volume was mounted inside the Nginx container at /usr/share/nginx/html. In the PHP-FPM container, that same volume was mounted at /var/www/html.

I corrected the Nginx document root and configured SCRIPT_FILENAME to use the PHP-FPM container's path. Then I validated the Nginx configuration, reloaded Nginx, and copied the index.php file from the jump host into the shared volume.

Finally, I verified that the PHP file was accessible from both containers and checked the pod status and logs. This resolved the path mismatch and allowed Nginx to serve the application while PHP-FPM processed the PHP scripts.”

Important: Say that the issue was resolved only after you have verified that the website works.