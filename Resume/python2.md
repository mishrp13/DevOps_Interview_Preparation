```

- Developed a **Python-based configuration comparison tool** using JSON, PyYAML, and recursive dictionary traversal to automatically detect and report added, removed, and modified configuration parameters across YAML and JSON files, simplifying configuration change validation.


In my project, I developed a Python automation script to compare two versions of configuration files and identify configuration changes.
In DevOps, we frequently work with YAML and JSON files for Kubernetes, application configurations, and deployment settings. Manually comparing these files can be time-consuming, especially when they contain nested configurations.
To solve this, I wrote a Python script that supports both YAML and JSON formats. I used Python's built-in json module for JSON files and the PyYAML library for YAML files.
First, the script loads the old and new configuration files and converts their contents into Python dictionaries.
Then I implemented a recursive function that compares the keys in both dictionaries.
If a key exists only in the new configuration, the script reports it as added. If it exists only in the old configuration, it reports it as removed. If the same key exists in both files but the values are different, it reports the change.
For nested dictionaries, the function calls itself recursively, allowing it to compare deeply nested configuration parameters.
Finally, the script prints all detected changes with their complete configuration paths.
This helps identify configuration differences before deployments and reduces manual configuration review effort.

3. Explain your code step by step
Step 1: Load configuration files
ddef load_config(file):
    with open(file) as f:
        if file.endswith(".json"):
            return json.load(f)
        else:
            return yaml.safe_load(f)


Interview explanation:
"I created a function to load both JSON and YAML configuration files. Based on the file extension, it uses either json.load() or yaml.safe_load() to convert the configuration into Python objects, typically dictionaries."


Step 2: Compare keys
for key in old.keys() | new.keys():

Interview explanation:
"I used the union operator | to get all unique keys from both dictionaries. This ensures the comparison can identify keys that are added, removed, or present in both files."
Step 3: Identify added and removed keys

if key not in old:
    print(f"Added: {current} = {new[key]}")

elif key not in new:
    print(f"Removed: {current} = {old[key]}")

Interview explanation:
"If a key is missing from the old configuration, it is considered added. If it is missing from the new configuration, it is considered removed."


Step 4: Compare nested dictionaries using recursion

elif isinstance(old[key], dict) and isinstance(new[key], dict):
    compare(old[key], new[key], current)


Interview explanation:
"This is the most important part of my script. If both values are dictionaries, the function calls itself to compare their nested keys. This is called recursion, and it allows the script to handle deeply nested YAML or JSON configurations."
Step 5: Identify changed values
elif old[key] != new[key]:
    print(f"Changed: {current}: {old[key]} -> {new[key]}")

Interview explanation:
"If a key exists in both configurations but its value has changed, the script displays the old and new values along with the complete key path."

4. Example you can demonstrate in an interview
old.yaml
app:
  name: nginx
  replicas: 2
  resources:
    cpu: 500m

new.yaml
app:
  name: nginx
  replicas: 3
  resources:
    cpu: 1000m

Output:
Changed: app.replicas: 2 -> 3
Changed: app.resources.cpu: 500m -> 1000m

Explain:
"The script detected that the replica count increased from 2 to 3 and the CPU configuration changed from 500m to 1000m. It ignored the application name because that value remained unchanged."
5. Interview follow-up questions

Why did you use recursion?
YAML and JSON configurations can contain nested dictionaries. Recursion allows the same comparison function to process nested levels without writing separate loops for each level.

What is the purpose of yaml.safe_load()?
It parses YAML using PyYAML's safe loader, avoiding the construction of arbitrary Python objects through unsafe YAML tags.
What is the difference between json.load() and json.loads()?
json.load() reads JSON from a file-like object, while json.loads() parses JSON from a string.
Can your script compare lists?
Yes, but only as complete values. If one list element changes, it reports the entire list as changed. It doesn't identify individual changed list elements.
Can you integrate this into a CI/CD pipeline?
Yes. I could execute it in Jenkins or GitHub Actions before deployment. To fail a pipeline when changes violate a policy, I would extend it to return a non-zero exit code.
What improvements would you make?
I would add command-line arguments, file validation, exception handling, deterministic output ordering, list-level comparisons, and an option to generate a JSON or HTML difference report.

6. Short 30-second answer to memorize
I developed a Python automation script to compare YAML and JSON configuration files. The script loads both configurations into Python dictionaries and uses recursion to compare nested keys. It identifies added, removed, and modified parameters and prints their complete configuration paths. This is useful in DevOps for identifying configuration changes between different versions of application or infrastructure configuration files before deployment.

One important point: Your current script is a comparison and reporting tool. It does not automatically block deployments or integrate with Jenkins unless you've added that functionality separately. In an interview, describe those as possible improvements rather than existing features.