```
•How do you manage dependencies (requirements.txt, pinning versions)?

Interview-ready answer

“In Python, I manage dependencies using a requirements.txt file or, in modern projects, tools like Poetry or pip-tools. For production and CI/CD, I prefer pinning dependency versions so that the same versions are installed across developer machines, CI pipelines, staging, and production.

For example, instead of:

requests

I would use:

requests==2.32.3

This prevents a newer version from being automatically installed and potentially breaking the application.

I typically create a virtual environment, install dependencies using pip, and generate or update the requirements file. In CI/CD, I install dependencies with pip install -r requirements.txt. I also separate runtime and development dependencies when appropriate.

For security and maintenance, I periodically update dependencies, test them in CI, and scan them for known vulnerabilities using tools such as pip-audit. The main goal is reproducible, secure builds across environments.”

1. What is requirements.txt?

It is a file that lists the Python packages your application needs.

Example:

flask==3.0.3
requests==2.32.3
boto3==1.35.24
PyYAML==6.0.2

Then anyone—or your CI/CD pipeline—can install exactly those dependencies:

pip install -r requirements.txt
2. Why pin versions?

Suppose today you install:

pip install requests

You might get:

requests 2.32.3

But six months later, the latest version might be:

requests 2.35.x

If that newer version introduces a breaking change, your application may behave differently.

So you pin:

requests==2.32.3

Now your development, CI, staging, and production environments can use the same version.

DevOps keyword: reproducibility.

3. Different levels of pinning

You may be asked about this.

requests

No pinning — potentially gets the latest version.

requests>=2.30

Minimum version only.

requests==2.32.3

Exact pinning.

For production environments, exact pinning is generally preferable when you want highly reproducible builds.

4. How would you use it in a CI/CD pipeline?

A typical pipeline could look like:

steps:
  - checkout

  - install_dependencies:
      run: |
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt

  - test:
      run: pytest

  - security_scan:
      run: pip-audit

  - build:
      run: docker build -t myapp .

The important point is that CI installs the same dependency versions defined by the project, rather than installing random/latest versions.

5. What about transitive dependencies?

This is an important DevOps interview point.

If you have:

Flask==3.0.3

Flask itself depends on other packages. Those are transitive dependencies.

For more deterministic builds, you can use tools such as pip-tools to generate a fully pinned requirements file.

For example, you might maintain:

# requirements.in
flask
requests

and use pip-compile to generate a locked requirements.txt containing the exact versions of Flask, Requests, and their dependencies.

This gives you better reproducibility.

6. Development vs production dependencies

You might have:

requirements.txt
requirements-dev.txt

Production:

# requirements.txt
flask==3.0.3
gunicorn==22.0.0
requests==2.32.3

Development:

# requirements-dev.txt
-r requirements.txt
pytest==8.3.3
black==24.8.0
ruff==0.6.5

Then:

pip install -r requirements.txt

for production, while developers/CI can use:

pip install -r requirements-dev.txt
7. Don't forget security

A strong DevOps answer should mention that pinning alone doesn't mean dependencies are secure.

You need to regularly update them and scan for vulnerabilities.

For example:

pip-audit

You can incorporate this into CI/CD:

Developer → Git → CI
                 ↓
          Install dependencies
                 ↓
             Run tests
                 ↓
          Security scanning
                 ↓
             Build image
                 ↓
              Deploy
⭐ Best 30-second interview answer

If the interviewer asks this directly, I would say:

“For Python projects, I manage dependencies using requirements.txt, or tools such as pip-tools/Poetry for more advanced dependency management. I pin production dependencies to specific versions to make builds reproducible across development, CI, staging, and production. For example, requests==2.32.3. In CI/CD, I install them using pip install -r requirements.txt, run automated tests, and scan dependencies for vulnerabilities using tools such as pip-audit. I also regularly update and test dependencies rather than blindly using the latest versions.”

That answer hits the key DevOps interview keywords: dependency management, version pinning, reproducibility, CI/CD, security, and dependency updates.