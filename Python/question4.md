```

•Shallow copy vs deep copy?

For a Python + DevOps interview, this is important because you may use copies when manipulating configuration dictionaries, YAML/JSON data, environment settings, deployment configs, etc.

Shallow copy vs Deep copy

The key difference is what happens to nested objects.

1. Shallow copy

A shallow copy creates a new outer object, but nested objects are still shared.

import copy

original = {
    "app": "nginx",
    "ports": [80, 443]
}

shallow = copy.copy(original)

shallow["ports"].append(8080)

print(original)
# {'app': 'nginx', 'ports': [80, 443, 8080]}

Why did original change?

Because:

original ──→ dictionary
              │
              └──→ ports list ←── shallow

The dictionaries are different, but both point to the same nested list.

2. Deep copy

A deep copy creates a new outer object and recursively copies nested objects.

import copy

original = {
    "app": "nginx",
    "ports": [80, 443]
}

deep = copy.deepcopy(original)

deep["ports"].append(8080)

print(original)
# {'app': 'nginx', 'ports': [80, 443]}

print(deep)
# {'app': 'nginx', 'ports': [80, 443, 8080]}

Now the nested list is also independent.

original ──→ dictionary ──→ list [80, 443]

deep     ──→ dictionary ──→ list [80, 443]
Interview-friendly comparison
	|                                       | Shallow copy    | Deep copy              |
| ------------------------------------- | --------------- | ---------------------- |
| Outer object                          | New             | New                    |
| Nested objects                        | **Shared**      | **Copied recursively** |
| `copy.copy()`                         | ✅               |                        |
| `copy.deepcopy()`                     |                 | ✅                      |
| Nested modification affects original? | Usually **yes** | **No**                 |
| Memory usage                          | Lower           | Higher                 |
| Performance                           | Faster          | Slower                 |

Very common interview trap
a = [[1, 2], [3, 4]]

b = a.copy()

b[0].append(99)

print(a)

Output:

[[1, 2, 99], [3, 4]]

Even though b = a.copy() creates a new outer list, the inner lists are shared.

Why does this matter in DevOps?

Imagine you have a deployment configuration:

config = {
    "app": {
        "name": "myapp",
        "replicas": 3
    },
    "environment": "prod"
}

You want to create a modified configuration for staging.

With a shallow copy:

import copy

staging = copy.copy(config)

staging["app"]["replicas"] = 1

You can accidentally change:

config["app"]["replicas"]

as well, because the nested "app" dictionary is shared.

For an independent configuration:

staging = copy.deepcopy(config)
staging["app"]["replicas"] = 1

Now the production configuration remains unchanged.

This can matter when you're manipulating Ansible-style variables, Kubernetes configuration data, Terraform-related Python automation, CI/CD configuration, or API payloads.

⭐ Best interview answer

If the interviewer asks "What's the difference between shallow and deep copy?", you can say:

"A shallow copy creates a new outer object but keeps references to the same nested objects. A deep copy recursively creates copies of nested objects as well. So if I modify a nested mutable object in a shallow copy, the original can also be affected, whereas with a deep copy it won't be."

Then give this tiny example:

import copy

a = {"x": [1, 2]}

b = copy.copy(a)
c = copy.deepcopy(a)

b["x"].append(3)

print(a)  # {'x': [1, 2, 3]}
print(c)  # {'x': [1, 2]}

One-line memory trick:

Shallow = new container, shared children.
Deep = new container, new children.