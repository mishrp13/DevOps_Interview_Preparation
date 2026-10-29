
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
