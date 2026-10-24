
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
