
import psutil
import time
import logging

# Configure logging
logging.basicConfig(
    filename="cpu_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CPU_THRESHOLD = 90


def monitor_cpu():

    print("Checking server CPU utilization...")

    # Get overall CPU usage
    total_cpu = psutil.cpu_percent(interval=1)

    print(f"\nOverall CPU Usage: {total_cpu}%")

    if total_cpu >= CPU_THRESHOLD:

        print("\nALERT: High CPU utilization detected!")

        process_list = []

        # Collect process information
        for process in psutil.process_iter(
            ['pid', 'name', 'username', 'memory_percent']
        ):

            try:
                cpu_usage = process.cpu_percent(interval=None)

                process_list.append({
                    'pid': process.info['pid'],
                    'name': process.info['name'],
                    'username': process.info['username'],
                    'cpu': cpu_usage,
                    'memory': process.info['memory_percent']
                })

            except (psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess):
                continue

        # Sort processes by CPU usage
        process_list.sort(
            key=lambda x: x['cpu'],
            reverse=True
        )

        print("\nTop 5 CPU-consuming processes:")

        for process in process_list[:5]:

            print("--------------------------------")

            print(f"PID: {process['pid']}")
            print(f"Process: {process['name']}")
            print(f"User: {process['username']}")
            print(f"CPU Usage: {process['cpu']}%")
            print(f"Memory Usage: {process['memory']:.2f}%")

            logging.warning(
                f"High CPU process: {process['name']} "
                f"PID: {process['pid']} "
                f"CPU: {process['cpu']}%"
            )

    else:

        print("Server CPU utilization is normal.")

        logging.info(
            f"CPU utilization is normal: {total_cpu}%"
        )


if __name__ == "__main__":
    monitor_cpu()
