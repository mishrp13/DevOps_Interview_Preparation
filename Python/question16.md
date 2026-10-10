```
•How do you read/write JSON, YAML, CSV?

Python for DevOps Interview: Reading and Writing JSON, YAML, and CSV
In a DevOps interview, you may be asked how Python reads configuration files, updates deployment settings, processes server inventories, or generates reports.
The key is to explain which module you use, how you read and write files, and where you use each format in DevOps automation.
1. JSON — JavaScript Object Notation
Interview answer: JSON is commonly used to exchange structured data between applications and REST APIs. In Python, we use the built-in json module to read, write, and modify JSON data.
Example file: config.json
{
  "app": "payment-api",
  "port": 8080,
  "replicas": 3
}


Read JSON

import json

with open("config.json", "r") as f:
    data = json.load(f)

print(data["app"])
print(data["port"])



Output:
payment-api
8080


Write JSON
import json

data = {
    "app": "payment-api",
    "port": 8080,
    "replicas": 5
}

with open("config.json", "w") as f:
    json.dump(data, f, indent=4)



Important interview questions
Q1. What is the difference between json.load() and json.loads()?
- json.load(f) reads JSON from a file object.
- json.loads(s) parses a JSON string.
Q2. What is the difference between json.dump() and json.dumps()?
- json.dump(data, f) writes JSON to a file.
- json.dumps(data) converts Python data into a JSON string.
Q3. What is the DevOps use case?
Reading API responses from cloud platforms, processing deployment metadata, and generating machine-readable reports.

2. YAML — YAML Ain't Markup Language
Interview answer: YAML is a human-readable configuration format widely used in Kubernetes, Ansible, and Docker Compose. In Python, I use the PyYAML library to parse and write YAML files.
Install the library:
pip install PyYAML


Example file: deployment.yaml
app: payment-api
replicas: 3
environment: production


Read YAML


import yaml

with open("deployment.yaml", "r") as f:
    data = yaml.safe_load(f)

print(data["app"])
print(data["replicas"])



Write YAML

import yaml

data = {
    "app": "payment-api",
    "replicas": 5,
    "environment": "production"
}

with open("deployment.yaml", "w") as f:
    yaml.safe_dump(data, f, sort_keys=False)



Important interview questions
Q1. Why do we use yaml.safe_load()?

It limits YAML construction to standard safe data types rather than allowing arbitrary Python object construction from YAML tags. It is the preferred default for ordinary configuration files.

Q2. What is the difference between JSON and YAML?
- JSON has stricter syntax and is commonly used in APIs.
- YAML supports comments and is generally easier for humans to maintain as configuration.
- Both can represent nested dictionaries and lists.

Q3. What is the DevOps use case?
Reading or updating Kubernetes manifests, generating configuration files, and automating infrastructure configuration.
Important: YAML indentation matters. Also, loading and rewriting a YAML file may remove its original comments or change formatting.

3. CSV — Comma-Separated Values
Interview answer: CSV stores tabular data in rows and columns. In Python, I use the built-in csv module to process server inventories, deployment reports, and monitoring exports.
Example file: servers.csv
hostname,ip,environment
web01,10.0.0.10,prod
web02,10.0.0.11,dev
db01,10.0.0.20,prod


Read CSV


import csv

with open("servers.csv", "r", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        print(row["hostname"], row["environment"])


Write CSV


import csv

servers = [
    {"hostname": "web01", "ip": "10.0.0.10"},
    {"hostname": "db01", "ip": "10.0.0.20"}
]

with open("report.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["hostname", "ip"]
    )
    writer.writeheader()
    writer.writerows(servers)



Important interview questions
Q1. What is the difference between csv.reader() and csv.DictReader()?
- csv.reader() returns each row as a list.
- csv.DictReader() returns each row as a dictionary keyed by column names.
Q2. Why do we use newline=""?
It lets Python's CSV module handle newline conventions correctly and helps avoid extra blank lines, especially when writing CSV files on Windows.
Q3. What is the DevOps use case?
Processing server inventories, filtering production hosts, exporting deployment results, and generating operational reports.

4. Quick revision table
| Interview Topic | JSON | YAML | CSV |
|---|---|---|---|
| Python module | `json` | `yaml` / PyYAML | `csv` |
| Installation | Built-in | `pip install PyYAML` | Built-in |
| Read | `json.load()` | `yaml.safe_load()` | `csv.DictReader()` |
| Write | `json.dump()` | `yaml.safe_dump()` | `csv.DictWriter()` |
| Best suited for | APIs and structured data | Infrastructure configuration | Tabular data |
| DevOps example | Cloud API response | Kubernetes manifest | Server inventory |


5. Most important practical interview question
Question: How would you read a server inventory CSV and generate a JSON file containing only production servers?

A strong answer is to explain the approach first, then write the code.

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

print(f"Exported {len(production_servers)} production servers")



What the interviewer is testing:
- File handling with with open().
- Reading structured data with the correct module.
- Iterating through records using a loop.
- Filtering with an if condition.
- Converting data from CSV records into JSON output.
This is a realistic DevOps automation task because it combines file handling, data structures, loops, and conditional logic.

Final interview tip: Don't just memorize the function names. Be ready to explain how you would read a configuration file, validate its contents, change a value, and write the updated result without accidentally overwriting the wrong environment's configuration.