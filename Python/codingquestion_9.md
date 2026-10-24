```
Parse `kubectl get pods` output and restart pods in CrashLoopBackOff ?

This is a common DevOps automation interview scenario involving Python, Kubernetes, subprocess, and error handling.


import subprocess

# Step 1: Get pods
result = subprocess.run(
    ["kubectl", "get", "pods", "--no-headers"],
    capture_output=True,
    text=True
)

# Step 2: Check command success
if result.returncode != 0:
    print("Error:", result.stderr)
    exit(1)

# Step 3: Parse output
for line in result.stdout.splitlines():
    columns = line.split()

    pod_name = columns[0]

    # Step 4: Find CrashLoopBackOff pods
    if "CrashLoopBackOff" in columns:
        print(f"Restarting pod: {pod_name}")

        # Step 5: Delete pod for controller recreation
        subprocess.run(
            ["kubectl", "delete", "pod", pod_name],
            check=True
        )


Note: This example assumes the default tabular output, a selected namespace, and pods managed by a Deployment, ReplicaSet, or another controller. Deleting a standalone pod will not automatically recreate it.
2. Sample input and output
Suppose kubectl get pods returns:

NAME          READY   STATUS             RESTARTS   AGE
nginx-abc     1/1     Running            0          2d
backend-xyz   0/1     CrashLoopBackOff   5          10m
redis-123     1/1     Running            0          1d
api-456       0/1     CrashLoopBackOff   8          15m


The Python script identifies:
Restarting pod: backend-xyz
pod "backend-xyz" deleted

Restarting pod: api-456
pod "api-456" deleted


3. Explain the script in an interview
Python concept	                  Explanation
subprocess.run()	                 Executes the kubectl command
capture_output=True	                 Captures command output
text=True	                         Returns output as a string
splitlines()	                     Splits output into lines
split()	                             Separates columns
columns[0]	                         Extracts pod name
if "CrashLoopBackOff" in columns	 Detects unhealthy pods
kubectl delete pod	                 Deletes pod so its controller can recreate it



4. Production-level improvement (important for interviews)
A strong interviewer might ask:

Q: Is deleting a pod the correct solution for CrashLoopBackOff?

Answer: Not always. CrashLoopBackOff usually means the container repeatedly starts and crashes. Kubernetes already attempts to restart it with exponential backoff.

Before deleting a pod, investigate:
kubectl logs <pod-name> --previous
kubectl describe pod <pod-name>


Possible causes include incorrect environment variables, application errors, missing secrets, OOMKilled, and failing health probes.

For production automation, prefer kubectl get pods -o json over parsing human-readable columns. Add namespace support, logging, exception handling, a dry-run option, and safeguards against repeated deletion.


"I use Python's subprocess module to execute kubectl commands, capture the output, and parse pod information. I identify pods in CrashLoopBackOff and can delete controller-managed pods to trigger recreation. In production, I prefer JSON output, investigate the root cause, and implement error handling and safety checks before taking automated action."