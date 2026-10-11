```

Compare two JSON/YAML configs and print the differences

This is a common Python scripting question for DevOps engineers, especially when working with Kubernetes, Terraform, CI/CD pipelines, and application configuration files.

1. Interview question
Q: Write a Python script to compare two JSON or YAML configuration files and print the differences.
For example, you have two configuration files:

config_old.yaml
app: payment
replicas: 2
image: nginx:1.24
debug: true

config_new.yaml
app: payment
replicas: 4
image: nginx:1.25
debug: false

Expected output:
replicas: 2 -> 4
image: nginx:1.24 -> nginx:1.25
debug: True -> False

This helps identify configuration changes before deployment.

. Simple Python solution for JSON
Python has a built-in json module.

import json

with open("old.json") as f:
    old = json.load(f)

with open("new.json") as f:
    new = json.load(f)

for key in old.keys() | new.keys():
    old_value = old.get(key)
    new_value = new.get(key)

    if old_value != new_value:
        print(f"{key}: {old_value} -> {new_value}")


Explanation
1. json.load() reads a JSON file and converts it into a Python object, usually a dictionary for config files.
2. old.keys() | new.keys() combines all unique keys from both dictionaries.
3. .get(key) retrieves values without raising KeyError for missing keys.
4. != checks whether the values are different.
5. print() displays the changes.

Interview note: This simple solution works for flat configurations. However, .get() cannot distinguish a missing key from a key whose value is None. For production scripts, handle added and removed keys separately.

YAML comparison using Python
YAML requires an external library, commonly PyYAML.
Install:

pip install pyyaml

Python script:

import yaml

with open("old.yaml") as f:
    old = yaml.safe_load(f)

with open("new.yaml") as f:
    new = yaml.safe_load(f)

for key in old.keys() | new.keys():
    if old.get(key) != new.get(key):
        print(
            f"{key}: {old.get(key)} -> {new.get(key)}"
        )

Why yaml.safe_load()?
It safely parses standard YAML data without constructing arbitrary Python objects. Prefer it over yaml.load() with an unsafe loader, particularly for untrusted files.


4. Production-style solution — Compare nested JSON/YAML
In real DevOps projects, configuration files are often nested.
Example Kubernetes-like configuration:

YAML

app:
  name: payment
  replicas: 3
  resources:
    cpu: 500m
    memory: 512Mi

A simple top-level comparison would report the entire app object as changed. A recursive comparison identifies exactly which nested fields changed.

import json
from pathlib import Path
import yaml

MISSING = object()

def load_config(filename):
    path = Path(filename)

    with path.open() as f:
        if path.suffix.lower() == ".json":
            return json.load(f)
        elif path.suffix.lower() in (".yaml", ".yml"):
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file format")

def compare(old, new, path=""):
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(old.keys() | new.keys()):
            field = f"{path}.{key}" if path else str(key)

            a = old.get(key, MISSING)
            b = new.get(key, MISSING)

            if a is MISSING:
                print(f"ADDED: {field} = {b}")
            elif b is MISSING:
                print(f"REMOVED: {field} = {a}")
            else:
                compare(a, b, field)

    elif old != new:
        print(f"CHANGED: {path}: {old} -> {new}")

old = load_config("old.yaml")
new = load_config("new.yaml")

compare(old, new)


This handles nested dictionaries, added keys, and removed keys. Lists are compared as whole values rather than element by element.
Example output
CHANGED: app.replicas: 2 -> 4
CHANGED: app.resources.cpu: 250m -> 500m
ADDED: app.resources.memory = 512Mi
REMOVED: app.debug = True


