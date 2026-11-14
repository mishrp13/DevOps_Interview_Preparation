```
We are working on an application that will be deployed on multiple containers within a pod on Kubernetes cluster. There is a requirement to share a volume among the containers to save some temporary data. The Nautilus DevOps team is developing a similar template to replicate the scenario. Below you can find more details about it.



Create a pod named volume-share-nautilus.


For the first container, use image ubuntu with latest tag only and remember to mention the tag i.e ubuntu:latest, container should be named as volume-container-nautilus-1, and run a sleep command for it so that it remains in running state. Volume volume-share should be mounted at path /tmp/news.


For the second container, use image ubuntu with the latest tag only and remember to mention the tag i.e ubuntu:latest, container should be named as volume-container-nautilus-2, and again run a sleep command for it so that it remains in running state. Volume volume-share should be mounted at path /tmp/cluster.


Volume name should be volume-share of type emptyDir.


After creating the pod, exec into the first container i.e volume-container-nautilus-1, and just for testing create a file news.txt with the content Welcome to xFusionCorp Industries under the mounted path of first container i.e /tmp/news.


The file news.txt should be present under the mounted path /tmp/cluster on the second container volume-container-nautilus-2 as well, since they are using a shared volume.


Note: The kubectl utility on the jump-host has been configured to work with the Kubernetes cluster.



sol:

I recently worked on a Kubernetes task where I had to share temporary data between two containers running inside the same Pod.

First, I created a Pod manifest with two Debian containers. I configured both containers to use the same EmptyDir volume named `volume-share`.

I mounted the shared volume at `/tmp/official` in the first container and `/tmp/games` in the second container.

I also configured `sleep infinity` as the container command to ensure both containers remained running.

After creating the Pod using `kubectl create -f file.yaml`, I verified that both containers were ready using `kubectl get pods`.

Next, I used `kubectl exec` to enter the first container and created a file named `official.txt` inside `/tmp/official`.

Then I executed a command inside the second container and checked `/tmp/games`. The same file was present there, and I verified its contents using the `cat` command.

This confirmed that both containers were successfully sharing data through the same EmptyDir volume.

Through this task, I demonstrated how Kubernetes supports data sharing between multiple containers within a single Pod using shared volumes.

final: 

kubectl exec volume-share-devops -c volume-container-devops-1 -- sh -c 'echo "Welcome to xFusionCorp Industries" > /tmp/beta/beta.txt'

kubectl exec volume-share-devops -c volume-container-devops-2 -- cat /tmp/games/beta.txt