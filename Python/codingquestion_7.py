import json
import yaml

def load_config(file):
    with open(file) as f:
        if file.endswith(".json"):
            return json.load(f)
        else:
            return yaml.safe_load(f)

def compare(old, new, path=""):
    for key in old.keys() | new.keys():
        current = f"{path}.{key}" if path else key

        if key not in old:
            print(f"Added: {current} = {new[key]}")

        elif key not in new:
            print(f"Removed: {current} = {old[key]}")

        elif isinstance(old[key], dict) and isinstance(new[key], dict):
            compare(old[key], new[key], current)

        elif old[key] != new[key]:
            print(f"Changed: {current}: {old[key]} -> {new[key]}")

old = load_config("old.yaml")
new = load_config("new.yaml")

compare(old, new)



# old.yaml
# app:
#   name: nginx
#   replicas: 2
#   resources:
#     cpu: 500m


# new.yaml
# app:
#   name: nginx
#   replicas: 3
#   resources:
#     cpu: 1000m


# Output
# Changed: app.replicas: 2 -> 3
# Changed: app.resources.cpu: 500m -> 1000m


# Interview explanation:
# I use recursion to compare nested dictionaries. If both values are dictionaries, 
# the function calls itself to compare their nested keys. Otherwise, it checks for added, 
# removed, or changed values.

# Note: This handles nested dictionaries. Lists are compared as whole values, which is
# sufficient for a basic nested-config interview question.


