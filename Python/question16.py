#1. JSON — Read and Write
import json

# Read JSON
with open("config.json", "r") as f:
    data = json.load(f)

print(data)

# Modify data
data["replicas"] = 5

# Write JSON
with open("config.json", "w") as f:
    json.dump(data, f, indent=4)




#2. YAML — Read and Write
import yaml

# Read YAML
with open("deployment.yaml", "r") as f:
    data = yaml.safe_load(f)

print(data)

# Modify data
data["replicas"] = 5

# Write YAML
with open("deployment.yaml", "w") as f:
    yaml.safe_dump(data, f, sort_keys=False)




#Install dependency: pip install PyYAML
#3. CSV — Read and Write
import csv

# Read CSV
with open("servers.csv", "r", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        print(row)

# Write CSV
servers = [
    {"hostname": "web01", "ip": "10.0.0.10"},
    {"hostname": "web02", "ip": "10.0.0.11"}
]

with open("report.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=["hostname", "ip"]
    )
    writer.writeheader()
    writer.writerows(servers)




#4. DevOps Interview Example — Filter Production Servers from CSV
import csv
import json

production_servers = []

with open("servers.csv", "r", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        if row["environment"] == "prod":
            production_servers.append(row)

with open("production_servers.json", "w") as f:
    json.dump(production_servers, f, indent=4)

print("Production server report generated")