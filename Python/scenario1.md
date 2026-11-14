```
Think of the script as 5 steps
1. Import libraries
   
   Get tools for CPU monitoring, time-related operations, and logging.
2. Configure logging
   
   Store monitoring information in cpu_monitor.log.
3. Check CPU usage
   
   Get the overall CPU utilization using psutil.
4. Apply condition
   
   If CPU is greater than or equal to 90%, trigger an alert.
5. Find top processes
   
   Collect process details, sort by CPU usage, display the top 5, and log them.




Your production server reaches 95% CPU utilization. Write a Python script to identify which process is consuming the maximum CPU.

This is one of the most common Python + DevOps interview scenarios. Let's solve it in a way that demonstrates practical production troubleshooting skills.
Scenario: Production server CPU utilization reaches 95%
Interviewer asks:

Your production Linux server suddenly reaches 95% CPU utilization. You need to identify which process is consuming the maximum CPU. How would you automate this using Python?
1. Interview-ready explanation
"I would use Python's psutil library to monitor system CPU utilization and identify the processes consuming the highest CPU resources.

First, I would check the overall CPU utilization. If it crosses a threshold, such as 90%, I would collect process-level CPU statistics, sort processes by CPU consumption, and identify the top five CPU-consuming processes.

I would also capture the PID, process name, username, memory utilization, and CPU percentage.

Finally, I would log the results and send an alert to the DevOps team so that we can investigate the root cause."
2. Install the required Python library
Run:
pip install psutil


psutil allows Python to retrieve system and process-level information such as CPU, memory, disk, and network utilization.
3. Python script – Identify the highest CPU-consuming process
Interview-ready solution


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


4. Execute the script
Save the file as:
cpu_monitor.py


Execute:
python3 cpu_monitor.py


Example output:

Server CPU monitoring
High CPU alert

95%
Overall CPU utilization (example output)

Top CPU-consuming processes
PID	Process	CPU
1250	python3	65%
2350	java	20%
1450	nginx	8%
1600	redis	4%
1800	node	2%

Illustrative output; actual process usage depends on the server.

5. Explain the important Python functions
Function	Purpose
psutil.cpu_percent()	Gets overall CPU utilization
psutil.process_iter()	Iterates through running processes
process.cpu_percent()	Gets process CPU utilization
process.memory_percent()	Gets process memory utilization
process.pid	Identifies process ID
sort()	Sorts processes by CPU usage
logging.warning()	Records high CPU alerts

Important technical point: The first call to process.cpu_percent(interval=None) may return 0 because it needs a previous measurement. For accurate process-level readings, take an initial CPU measurement, wait for an interval, and then collect the second measurement. Also, process CPU percentages can exceed 100% on multicore systems because they are measured per logical CPU.
6. Linux commands to cross-check your Python results
In a real DevOps environment, I would also validate the results using Linux commands.

top


Displays real-time CPU and memory usage.
ps aux --sort=-%cpu | head -10


Displays the top CPU-consuming processes.
htop


Provides an interactive process monitoring view.
pidstat 1


Shows process-level CPU statistics at one-second intervals (requires sysstat).
7. Follow-up questions interviewer may ask
Prepare these carefully:
1. What is the difference between psutil.cpu_percent() and process.cpu_percent()?
2. How would you continuously monitor CPU utilization every 60 seconds?
3. How would you send an email or Slack alert when CPU exceeds 90%?
4. How would you monitor 100 Linux servers simultaneously?
5. How would you identify a process consuming high CPU for more than five minutes?
6. Would you automatically kill a process consuming 95% CPU? Why or why not?
7. How would you execute this Python script through a Jenkins pipeline or cron job?

--------------------------------------------------------------------------

psutil → CPU and process information.



logging → Save alerts.



time → Time-related operations (although your current script doesn't actually use it).