```
Write a CLI that takes --env and --service and triggers a deployment?



import argparse
import subprocess
import sys

def deploy(env, service):
    print(f"Deploying {service} to {env} environment...")

    try:
        subprocess.run(
            [
                "kubectl", "rollout", "restart",
                f"deployment/{service}",
                "-n", env
            ],
            check=True
        )

        print("Deployment triggered successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Deployment failed: {e}")
        sys.exit(1)

    except FileNotFoundError:
        print("Error: kubectl is not installed.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="DevOps Deployment CLI"
    )

    parser.add_argument(
        "--env",
        required=True,
        choices=["dev", "qa", "staging", "prod"],
        help="Target environment"
    )

    parser.add_argument(
        "--service",
        required=True,
        help="Service name"
    )

    args = parser.parse_args()

    deploy(args.env, args.service)


if __name__ == "__main__":
    main()


How to execute
Save the script as deploy.py.

Run the following command:

python deploy.py --env dev --service payment

Expected output:

Deploying payment to dev environment...
Deployment triggered successfully!

This triggers the Kubernetes command:

kubectl rollout restart deployment/payment -n dev

Here, dev is the Kubernetes namespace and payment is the deployment name. The script assumes the namespace matches the environment and that kubectl is configured with access to the correct cluster.

Component	                        Explanation
argparse	                        Accepts CLI arguments
--env	                            Specifies deployment environment
--service                           Specifies application/service
required=True	                    Makes both arguments mandatory
choices	                            Restricts environment values
subprocess.run()	                Executes the Kubernetes command
check=True	                        Raises an error for a failed command
try-except	                        Handles deployment command failures


Interview answer (speak confidently)
"I would use Python's argparse module to build a command-line interface that accepts environment and service arguments. I would validate the environment and use subprocess.run to execute a Kubernetes deployment command. I would also add exception handling, logging, and deployment status verification to make the script reliable."