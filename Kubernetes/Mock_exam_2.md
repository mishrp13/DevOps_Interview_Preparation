```

Task1:

From student-node ssh cluster1-controlplane to solve this question.


Create a StorageClass named local-sc with the following specifications and set it as the default storage class:

The provisioner should be kubernetes.io/no-provisioner
The volume binding mode should be WaitForFirstConsumer
Volume expansion should be enabled

Sol:

Solution
Check kubernetes.io documentation on StorageClasses

On cluster1-controlplane:

Create the StorageClass YAML file:
# local-sc.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-sc
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true

Apply the manifest on the specified cluster:
ssh cluster1-controlplane
kubectl apply -f local-sc.yaml

Verify the StorageClass
kubectl get storageclass

You should see local-sc marked as (default) with the correct provisioner and settings

-------------------------------------------------------------------------------------

Task2. 



From student-node ssh cluster1-controlplane to solve this question.


Create a deployment named logging-deployment in the namespace logging-ns with 1 replica, with the following specifications:

1) The main container must be named app-container, use the image busybox, and start by creating a log directory /var/log/app and run the below command to simulate generating logs:

while true; do 
  echo "Log entry" >> /var/log/app/app.log
  sleep 5
done

2) Add a co-located container named log-agent that also uses the busybox image and runs these commands:

touch /var/log/app/app.log
tail -f /var/log/app/app.log

3) Both containers must share the same emptyDir volume mounted at /var/log/app.

4) Use any consistent label for the Deployment selector and the Pod template labels (the exact key/value is up to you, as long as they match).

log-agent logs should display the entries logged by the main app-container.


Solution
Create the Deployment YAML file, for example logger-deployment.yaml :
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logging-deployment
  namespace: logging-ns
spec:
  replicas: 1
  selector:
    matchLabels:
      app: logger
  template:
    metadata:
      labels:
        app: logger
    spec:
      volumes:
        - name: log-volume
          emptyDir: {}
      containers:
        - name: app-container
          image: busybox
          command: ["sh", "-c", "mkdir -p /var/log/app; while true; do echo 'Log entry' >> /var/log/app/app.log; sleep 5; done"]
          volumeMounts:
            - name: log-volume
              mountPath: /var/log/app
        - name: log-agent
          image: busybox
          command: ["sh", "-c", "touch /var/log/app/app.log; tail -f /var/log/app/app.log"]
          volumeMounts:
            - name: log-volume
              mountPath: /var/log/app

Apply the deployment:
kubectl apply -f logger-deployment.yaml

Verify that the log-agent container displays log entries:
kubectl logs -n logging-ns deployment/logging-deployment -c log-agent --tail=50

You should see repeated Log entry lines in the output.

------------------------------------------------------------------------------------------------

Task3.

From student-node ssh cluster1-controlplane to solve this question.


A Deployment named webapp-deploy is running in the ingress-ns namespace and is exposed via a Service named webapp-svc.

Create an Ingress resource called webapp-ingress in the same namespace that will route traffic to the service. The Ingress must:

Use pathType: Prefix
Route requests sent to path / to the backend service
Forward traffic to port 80 of the service
Be configured for the host kodekloud-ingress.app
Test app availablility using the following command:

curl -s http://kodekloud-ingress.app/

Solution:

Make sure the path is set correctly and the pathType is Prefix. Use host-based routing

Checkout the resources in the ingress-ns namespace:
ssh cluster1-controlplane
kubectl get deployment webapp-deploy -n ingress-ns
kubectl get svc webapp-svc -n ingress-ns

Create the Ingress YAML file:
# webapp-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
  namespace: ingress-ns
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: kodekloud-ingress.app
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: webapp-svc
            port:
              number: 80

Apply the Ingress resource:
kubectl apply -f webapp-ingress.yaml

Test access to the app:
curl http://kodekloud-ingress.app/

-----------------------------------------------------------------------------------------

4.
From student-node ssh cluster1-controlplane to solve this question.


Create a new deployment called nginx-deploy, with image nginx:1.16 and 1 replica. Next, upgrade the deployment to version 1.17 using rolling update.

Solution:

Explore the --record option while creating the deployment while working with the deployment definition file. Then make use of the kubectl apply command to create or update the deployment.

To create a deployment definition file nginx-deploy:

kubectl create deployment nginx-deploy --image=nginx:1.16 --dry-run=client -o yaml > deploy.yaml

To create a resource from definition file and to record:

kubectl apply -f deploy.yaml --record

To view the history of deployment nginx-deploy:

kubectl rollout history deployment nginx-deploy

To upgrade the image to next given version:

kubectl set image deployment/nginx-deploy nginx=nginx:1.17 --record

To view the history of deployment nginx-deploy:

kubectl rollout history deployment nginx-deploy

--------------------------------------------------------------------------------

5. 

From student-node ssh cluster1-controlplane to solve this question.


Create a new user called john. Grant him access to the cluster using a csr named john-developer. Create a role developer which should grant John the permission to create, list, get, update and delete pods in the development namespace . The private key exists in the location: /root/CKA/john.key and csr at /root/CKA/john.csr.

Important Note: As of kubernetes 1.19, the CertificateSigningRequest object expects a signerName.

Please refer to the documentation to see an example. The documentation tab is available at the top right of the terminal.

Solution:

Solution manifest file to create a CSR as follows:

---
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john-developer
spec:
  signerName: kubernetes.io/kube-apiserver-client
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZEQ0NBVHdDQVFBd0R6RU5NQXNHQTFVRUF3d0VhbTlvYmpDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRApnZ0VQQURDQ0FRb0NnZ0VCQUt2Um1tQ0h2ZjBrTHNldlF3aWVKSzcrVVdRck04ZGtkdzkyYUJTdG1uUVNhMGFPCjV3c3cwbVZyNkNjcEJFRmVreHk5NUVydkgyTHhqQTNiSHVsTVVub2ZkUU9rbjYra1NNY2o3TzdWYlBld2k2OEIKa3JoM2prRFNuZGFvV1NPWXBKOFg1WUZ5c2ZvNUpxby82YU92czFGcEc3bm5SMG1JYWpySTlNVVFEdTVncGw4bgpjakY0TG4vQ3NEb3o3QXNadEgwcVpwc0dXYVpURTBKOWNrQmswZWhiV2tMeDJUK3pEYzlmaDVIMjZsSE4zbHM4CktiSlRuSnY3WDFsNndCeTN5WUFUSXRNclpUR28wZ2c1QS9uREZ4SXdHcXNlMTdLZDRaa1k3RDJIZ3R4UytkMEMKMTNBeHNVdzQyWVZ6ZzhkYXJzVGRMZzcxQ2NaanRxdS9YSmlyQmxVQ0F3RUFBYUFBTUEwR0NTcUdTSWIzRFFFQgpDd1VBQTRJQkFRQ1VKTnNMelBKczB2czlGTTVpUzJ0akMyaVYvdXptcmwxTGNUTStsbXpSODNsS09uL0NoMTZlClNLNHplRlFtbGF0c0hCOGZBU2ZhQnRaOUJ2UnVlMUZnbHk1b2VuTk5LaW9FMnc3TUx1a0oyODBWRWFxUjN2SSsKNzRiNnduNkhYclJsYVhaM25VMTFQVTlsT3RBSGxQeDNYVWpCVk5QaGhlUlBmR3p3TTRselZuQW5mNm96bEtxSgpvT3RORStlZ2FYWDdvc3BvZmdWZWVqc25Yd0RjZ05pSFFTbDgzSkljUCtjOVBHMDJtNyt0NmpJU3VoRllTVjZtCmlqblNucHBKZWhFUGxPMkFNcmJzU0VpaFB1N294Wm9iZDFtdWF4bWtVa0NoSzZLeGV0RjVEdWhRMi80NEMvSDIKOWk1bnpMMlRST3RndGRJZjAveUF5N05COHlOY3FPR0QKLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tCg==
  usages:
  - digital signature
  - key encipherment
  - client auth

To approve this certificate, run: kubectl certificate approve john-developer

Next, create a role developer and rolebinding developer-role-binding, run the command:

kubectl create role developer --resource=pods --verb=create,list,get,update,delete --namespace=development

kubectl create rolebinding developer-role-binding --role=developer --user=john --namespace=development

To verify the permission from kubectl utility tool:

kubectl auth can-i update pods --as=john --namespace=development

---------------------------------------------------------------------------------------------

6.

From student-node ssh cluster1-controlplane to solve this question.


Create an nginx pod called nginx-resolver using the image nginx and expose it internally with a service called nginx-resolver-service. Test that you are able to look up the service and pod names from within the cluster. Use the image: busybox:1.28 for dns lookup. Record results in /root/CKA/nginx.svc and /root/CKA/nginx.pod

Solution:

Use the command kubectl run and create a nginx pod and busybox pod. Resolve it, nginx service and its pod name from busybox pod.

To create a pod nginx-resolver and expose it internally:

kubectl run nginx-resolver --image=nginx
kubectl expose pod nginx-resolver --name=nginx-resolver-service --port=80 --target-port=80 --type=ClusterIP

To create a pod test-nslookup. Test that you are able to look up the service and pod names from within the cluster:

kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never -- nslookup nginx-resolver-service
kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never -- nslookup nginx-resolver-service > /root/CKA/nginx.svc

Get the IP of the nginx-resolver pod and replace the dots(.) with hyphon(-) which will be used below.

kubectl get pod nginx-resolver -o wide
kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart

------------------------------------------------------------------------------------------

7.

From student-node ssh cluster1-controlplane to solve this question.


Create a static pod on cluster1-node01 called nginx-critical with the image nginx. Make sure that it is recreated/restarted automatically in case of a failure.

For example, use /etc/kubernetes/manifests as the static Pod path.

Solution:

To create a static pod called nginx-critical by using below command:

kubectl run nginx-critical --image=nginx --dry-run=client -o yaml > static.yaml

Copy the contents of this file or use scp command to transfer this file from cluster1-controlplane to cluster1-node01 node.

root@cluster1-controlplane:~# scp static.yaml cluster1-node01:/root/

To know the IP Address of the cluster1-node01 node:

root@cluster1-controlplane:~# kubectl get nodes -o wide

# Perform SSH
root@cluster1-controlplane:~# ssh cluster1-node01
OR
root@cluster1-controlplane:~# ssh <IP of cluster1-node01>

On cluster1-node01 node:

Check if static pod directory is present which is /etc/kubernetes/manifests, if it's not present then create it.

root@cluster1-node01:~# mkdir -p /etc/kubernetes/manifests

Add that complete path to the staticPodPath field in the kubelet config.yaml file.

root@cluster1-node01:~# vi /var/lib/kubelet/config.yaml

now, move/copy the static.yaml to path /etc/kubernetes/manifests/.

root@cluster1-node01:~# cp /root/static.yaml /etc/kubernetes/manifests/

Go back to the cluster1-controlplane node and check the status of static pod:

root@cluster1-node01:~# exit
logout
root@cluster1-controlplane:~# kubectl get pods 

----------------------------------------------------------------------------------------

8.


From student-node ssh cluster1-controlplane to solve this question.


Create a Horizontal Pod Autoscaler with name backend-hpa for the deployment named backend-deployment in the backend namespace with the webapp-hpa.yaml file located under the root folder.
Ensure that the HPA scales the deployment based on memory utilization, maintaining an average memory usage of 65% across all pods.
Configure the HPA with a minimum of 3 replicas and a maximum of 15.

Solution:

Under /root/ folder you will find a yaml file webapp-hpa.yaml. Update the yaml file as per task given.

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-deployment
  minReplicas: 3
  maxReplicas: 15
  metrics:
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 65

Use below command

kubectl create -f webapp-hpa.yaml

------------------------------------------------------------------------------------------------

9.

From student-node ssh cluster2-controlplane to solve this question.


As a Kubernetes administrator, you are unable to run any of the kubectl commands on the cluster. Troubleshoot the problem and get the cluster to a functioning state.

Solution:

Check if the node's kubelet service is running. Without it, the control plane cannot register nodes or accept kubectl requests.

SSH into the control plane node:
ssh cluster2-controlplane

Preview system logs to check for issues:
journalctl -xe

Check the status of the kubelet service:
systemctl status kubelet

You should see that the kubelet service is inactive or failed.

Start the kubelet service:
sudo systemctl start kubelet

Enable the kubelet to start on boot (optional):
sudo systemctl enable kubelet

Confirm that kubectl is functional again:
kubectl get nodes

------------------------------------------------------------------------------------------

10.

From student-node ssh cluster1-controlplane to solve this question.


Modify the existing web-gateway on cka5673 namespace to handle HTTPS traffic on port 443 for kodekloud.com, using a TLS certificate stored in a secret named kodekloud-tls.

Solution:

SSH into the cluster1-controlplane host

ssh cluster1-controlplane

Check the configuration of the web-gateway.

cluster1-controlplane ~ ➜  kubectl get gateway web-gateway -n cka5673 -o yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: web-gateway
  namespace: cka5673
spec:
  gatewayClassName: nginx
  listeners:
  - allowedRoutes:
      namespaces:
        from: Same
    name: https
    port: 80
    protocol: HTTP

The current configuration of the web-gateway is incorrect as it is listening on port 80 using the HTTP protocol. To update the web-gateway to listen on port 443 with the TLS certificate, use the following manifest:

# web-gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: web-gateway
  namespace: cka5673
spec:
  gatewayClassName: nginx
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      hostname: kodekloud.com
      tls:
        certificateRefs:
          - name: kodekloud-tls

Apply the configuration as follows:

kubectl apply -f web-gateway.yaml

-----------------------------------------------------------------------------------------
11.

From student-node ssh cluster1-controlplane to solve this question.


On the cluster, the team has installed multiple helm charts on a different namespace. By mistake, those deployed resources include one of the vulnerable images called kodekloud/webapp-color:v1. Find out the release name and uninstall it.

Solution:

In this task, we will use the helm commands and jq tool. Here are the steps: -



Run the helm ls command with -A option to list the releases deployed on all the namespaces using helm.
helm ls -A



We will use the jq tool to extract the image name from the deployments.
kubectl get deploy -n <NAMESPACE> <DEPLOYMENT-NAME> -o json | jq -r '.spec.template.spec.containers[].image'



Replace <NAMESPACE> with the namespace and <DEPLOYMENT-NAME> with the deployment name, which we get from the previous commands.

After finding the kodekloud/webapp-color:v1 image, use the helm uninstall to remove the deployed chart that are using this vulnerable image.


helm uninstall <RELEASE-NAME> -n <NAMESPACE> 

--------------------------------------------------------------------------------

12.

From student-node ssh cluster1-controlplane to solve this question.

You are requested to create a NetworkPolicy to allow traffic from frontend apps located in the frontend namespace, to backend apps located in the backend namespace, but not from the databases in the databases namespace. There are three policies available in the /root folder. Apply the most restrictive policy from the provided YAML files to achieve the desired result. Do not delete any existing policies.

Solution:

Read through all provided NetworkPolicy YAML files carefully. Only one of them restricts traffic from the databases namespace while allowing it from frontend.

On cluster1-controlplane, Review the contents of the three YAML files:
cat /root/net-pol-1.yaml
cat /root/net-pol-2.yaml
cat /root/net-pol-3.yaml

Understand the differences:
net-pol-1.yaml: Too broad; allows traffic from any namespace with a certain label.
net-pol-2.yaml: Incorrect; explicitly allows both frontend and databases.
net-pol-3.yaml: Correct; only allows traffic from the frontend namespace.
Apply the correct policy (net-pol-3.yaml):
kubectl apply -f /root/net-pol-3.yaml

Verify it’s the only one applied:
kubectl get netpol -n backend

You should only see net-policy-3 listed

-------------------------------------------------------------------------------------------

13.

From student-node ssh cluster3-controlplane to solve this question.


Your cluster has a failed deployment named backend-api with multiple pods. Troubleshoot the deployment so that all pods are in a running state. Do not make adjustments to the resource limits defined on the deployment pods.

NOTE: A ResourceQuota named cpu-mem-quota is applied to the default namespace and should not be edited or modified.

Solution:

SSH into the cluster3-controlplane host
ssh cluster3-controlplane

1. Check Deployment Status
Verify the current status of the deployment:

kubectl get deploy

Expected output (shows that only 2 out of 3 pods are running):

NAME          READY   UP-TO-DATE   AVAILABLE   AGE
backend-api   2/3     2            2           3m48s

The third pod is not getting scheduled.

2. Find the Root Cause
Describe the ReplicaSet to check why the third pod is not being created:

kubectl describe replicasets backend-api-7977bfdbd5

The issue is due to ResourceQuota limitations.
The namespace has a memory limit of 300Mi, and the deployment is exceeding it.
requests.memory=128Mi, used: requests.memory=256Mi, limited: requests.memory=300Mi
Warning  FailedCreate  Error creating: pods "backend-api-7977bfdbd5-hpcjw" is forbidden: exceeded quota: cpu-mem-quota, 
requested: requests.memory=128Mi, used: requests.memory=256Mi, limited: requests.memory=300Mi

3, Modify the Deployment to Fit Within the ResourceQuota
Edit the deployment and reduce memory requests:

kubectl edit deployment backend-api -n default

Modify the resources section:

resources:
  requests:
    cpu: "50m"   # Reduced from 100m to 50m
    memory: "90Mi"   # Reduced from 128Mi to 90Mi (Fits within quota)
  limits:
    cpu: "150m"   
    memory: "150Mi"

4. Verify the Pods (Still Only 2 Running)
Check if the new pod is scheduled:

kubectl get pods -n default

If the third pod is still missing, the old ReplicaSet might be preventing it.

5. Delete the Old ReplicaSet to Allow New Pods to Start
Find the old ReplicaSet:

kubectl get rs -n default

Delete the outdated ReplicaSet:

kubectl delete rs backend-api-7977bfdbd5 -n default

Wait for the new pods to come up.

6. Confirm All Pods Are Running
kubectl get pods -n default

-----------------------------------------------------------------------------------

14.


From student-node ssh cluster4-controlplane to solve this question.


Utilize the official Calico definition file, available at:

https://raw.githubusercontent.com/projectcalico/calico/v3.29.3/manifests/tigera-operator.yaml

to deploy the Calico CNI on the cluster.

Make sure to configure the CIDR to 172.17.0.0/16

After the CNI installation, verify that pods can successfully communicate.

Custom Definitions for calico can be retrieved via:

curl https://raw.githubusercontent.com/projectcalico/calico/v3.

Solution:

SSH into the cluster4-controlplane host
ssh cluster4-controlplane

1. Install the Calico CNI
Install the operator on your cluster:
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/tigera-operator.yaml

Note: If you used kubectl apply you might face the following error:
The CustomResourceDefinition "installations.operator.tigera.io" is invalid: metadata.annotations: Too long: may not be more than 262144 bytes

Download the custom resources necessary to configure Calico to set the CIDR to 172.17.0.0/16:
curl https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/custom-resources.yaml -O

Below is the structure of the final configuration:

# This section includes base Calico installation configuration.
# For more information, see: https://docs.tigera.io/calico/latest/reference/installation/api#operator.tigera.io/v1.Installation
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  # Configures Calico networking.
  calicoNetwork:
    ipPools:
    - name: default-ipv4-ippool
      blockSize: 26
      cidr: 172.17.0.0/16
      encapsulation: VXLANCrossSubnet
      natOutgoing: Enabled
      nodeSelector: all()

---

# This section configures the Calico API server.
# For more information, see: https://docs.tigera.io/calico/latest/reference/installation/api#operator.tigera.io/v1.APIServer
apiVersion: operator.tigera.io/v1
kind: APIServer
metadata:
  name: default
spec: {}

Apply the manifest by running the following command:
kubectl create -f custom-resources.yaml

Verify Calico installation in your cluster.
watch kubectl get pods -n calico-system

2. Test the pod-to-pod communication.
Run an nginx image:
kubectl run web-app --image nginx

Retrieve the IP address of the pod:
kubectl get pod web-app -o jsonpath='{.status.podIP}'

Test the connection:
kubectl run test --rm -it -n kube-public --image=jrecord/nettools 

---------------------------------------------------------------------------


```