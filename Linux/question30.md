```
•How do you write a bash script that takes arguments, checks the exit code and handles errors? (set -euo pipefail)

In a Linux DevOps interview, this question tests whether you can write a reliable Bash script that accepts arguments, detects failures, and exits with the correct status code.
The key concepts are:
- $1, $2, $# — command-line arguments.
- $? — exit code of the last command.
- set -euo pipefail — helps catch common script errors.
- if, ||, and exit — handle errors and report success or failure.
1. Example Bash script
Suppose you need a script that checks whether a service is running. It takes the service name as an argument.

#!/usr/bin/env bash

set -euo pipefail

# Check that an argument was provided
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <service-name>" >&2
    exit 1
fi

SERVICE="$1"

echo "Checking service: $SERVICE"

# Check whether the service is active
if systemctl is-active --quiet "$SERVICE"; then
    echo "SUCCESS: $SERVICE is running"
    exit 0
else
    rc=$?
    echo "ERROR: $SERVICE is not running (exit code: $rc)" >&2
    exit "$rc"
fi



Save it as check_service.sh.
Run it:
chmod +x check_service.sh
./check_service.sh nginx


If Nginx is running, it reports success. If the service is not active, it reports an error and returns a nonzero exit code.
Note: systemctl requires a system using systemd. Also, systemctl is-active may return nonzero for an inactive service, which is not necessarily the same as a script or system error.
2. Explain set -euo pipefail
This is one of the most important parts of the interview question.
set -euo pipefail


-e — Exit on many command failures
If a command fails, Bash generally exits instead of continuing.
set -e
ls /missing-directory
echo "This may not run"


Important: -e has exceptions, including commands used in if conditions, while tests, and certain &&/|| lists.


-u — Treat unset variables as errors
Prevents accidental use of variables that were never defined.
set -u
echo "$SERVICE_NAME"


If SERVICE_NAME is unset, Bash reports an error and exits.


-o pipefail — Detect failures inside pipelines
A pipeline normally returns the exit code of its last command. pipefail makes it return nonzero if a command in the pipeline fails.
set -o pipefail
cat missing.txt | sort
echo "$?"


Without pipefail, sort might succeed on empty input and hide the earlier cat failure. With pipefail, the pipeline returns a failure status.


Interview tip: These options improve reliability, but they do not replace explicit error handling. You still need to validate arguments and handle expected failures.
3. Understand arguments: $1, $#, and $@
Suppose you run:
./deploy.sh staging nginx


Variable	Meaning	                Value
$0	       Script name	         ./deploy.sh
$1	     First argument	             staging
$2	    Second argument	             nginx
$#	    Number of arguments	           2
"$@"	All arguments, kept separate   staging nginx


For example:
ENVIRONMENT="$1"
SERVICE="$2"


This stores the first argument in ENVIRONMENT and the second in SERVICE.
Always quote variables such as "$SERVICE" to prevent unwanted word splitting and wildcard expansion.
4. How to check an exit code
Linux commands return an exit status when they finish.
- 0 means success.
- A nonzero value means failure or another status, depending on the command.
Example:
systemctl is-active --quiet nginx
echo $?


If the command succeeds, the output is 0. If it fails, the output is nonzero.
You can also capture the status immediately:
some_command
rc=$?

if [[ "$rc" -eq 0 ]]; then
    echo "Command succeeded"
else
    echo "Command failed with exit code $rc" >&2
    exit "$rc"
fi


Here, rc stores the command's exit status. Capture $? immediately, because running another command changes it.
For commands whose failure you expect, an if condition is usually clearer:
if some_command; then
    echo "Success"
else
    rc=$?
    echo "Failed with code $rc" >&2
    exit "$rc"
fi


5. A more reusable DevOps script
This example takes an environment and a service name, validates the arguments, and checks the service.

#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 <environment> <service>" >&2
    echo "Example: $0 staging nginx" >&2
}

if [[ $# -ne 2 ]]; then
    usage
    exit 2
fi

ENVIRONMENT="$1"
SERVICE="$2"

echo "Environment: $ENVIRONMENT"
echo "Service: $SERVICE"

if systemctl is-active --quiet "$SERVICE"; then
    echo "SUCCESS: $SERVICE is active in $ENVIRONMENT"
else
    rc=$?
    echo "ERROR: $SERVICE is not active (exit code: $rc)" >&2
    exit "$rc"
fi

echo "Check completed"
exit 0



Run:
chmod +x check_service.sh
./check_service.sh staging nginx


Why this is useful:
- usage() prints the correct syntax.
- [[ $# -ne 2 ]] rejects missing or extra arguments.
- >&2 sends error messages to standard error.
- exit 2 indicates invalid usage.
- exit "$rc" propagates the service check's failure status.
- exit 0 explicitly indicates success.
6. Common interview mistakes
Mistake	                            Better practice
Forgetting to validate arguments	Check $# before using $1 or $2.
Checking $? too late	            Save it immediately in a variable.
Assuming set -e handles every error	Use explicit if statements for expected failures.
Ignoring failures inside pipelines	Use set -o pipefail.
Using unquoted variables	          Prefer "$VARIABLE".



Printing an error but returning success	Use exit with a nonzero status.


7. A strong interview answer
“I write Bash scripts with set -euo pipefail to catch many command failures, unset variables, and pipeline errors. I validate command-line arguments using $#, access arguments through $1 and $2, and check expected command failures using if statements. I capture the exit status using $? when needed, print errors to standard error, and return an appropriate nonzero exit code. This makes automation scripts more predictable in CI/CD pipelines and production environments.”
Remember: set -euo pipefail helps prevent silent failures, while explicit validation and error handling make the script robust.