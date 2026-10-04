```
1.Parse a log file and count errors by type or find the top 10 IPs


Absolutely. This is a very common Python + DevOps interview task because it tests whether you can combine:

file handling
string processing
regex
dictionaries / Counter
exception handling
command-line arguments
scalability for large log files

The interviewer may ask:

"Write a Python script to parse a log file and count errors by type."

or:

"Find the top 10 IP addresses from a log file."

Let's prepare both.

1. Count errors by type

Imagine a log file:

2026-10-04 10:01:01 ERROR ConnectionError Unable to connect to server
2026-10-04 10:01:05 INFO Deployment started
2026-10-04 10:01:10 ERROR TimeoutError AWS API timed out
2026-10-04 10:01:15 ERROR ConnectionError SSH connection failed
2026-10-04 10:01:20 ERROR PermissionError Access denied
2026-10-04 10:01:25 ERROR TimeoutError Request timed out

We want:

ConnectionError: 2
TimeoutError: 2
PermissionError: 1
2. Simple solution using Counter

Python's collections.Counter is perfect for this.

from collections import Counter

error_counts = Counter()

with open("app.log", "r") as file:

    for line in file:

        if "ERROR" in line:
            parts = line.split()

            error_type = parts[3]

            error_counts[error_type] += 1


for error, count in error_counts.items():
    print(f"{error}: {count}")

If the log is:

2026-10-04 10:01:01 ERROR ConnectionError Unable to connect
2026-10-04 10:01:10 ERROR TimeoutError AWS API timed out
2026-10-04 10:01:15 ERROR ConnectionError SSH failed
2026-10-04 10:01:20 ERROR PermissionError Access denied

Output:

ConnectionError: 2
TimeoutError: 1
PermissionError: 1
3. Why Counter?

You could use a normal dictionary:

counts = {}

if error_type in counts:
    counts[error_type] += 1
else:
    counts[error_type] = 1

But:

from collections import Counter

makes it much cleaner:

counts[error_type] += 1

And it gives you:

counts.most_common(10)

which is extremely useful for log-analysis questions.

4. Better interview version: most_common()
from collections import Counter

error_counts = Counter()

with open("app.log", "r") as file:

    for line in file:

        if "ERROR" in line:

            parts = line.split()
            error_type = parts[3]

            error_counts[error_type] += 1


print("Top errors:")

for error, count in error_counts.most_common(10):
    print(f"{error}: {count}")

This gives:

Top errors:
ConnectionError: 125
TimeoutError: 98
PermissionError: 42
DatabaseError: 31
5. But there's a problem with this solution

The interviewer might ask:

"What if the log file is 50 GB?"

Don't do:

content = file.read()

because that loads the entire file into memory.

Instead:

with open("app.log") as file:
    for line in file:
        process(line)

Python reads the file line by line.

This is an important DevOps interview point.

Good answer:

"For large log files, I would stream the file line by line rather than reading the entire file into memory. This keeps memory usage approximately constant."

6. Top 10 IP addresses

Now imagine an Apache/Nginx-style log:

192.168.1.10 - - [04/Oct/2026:10:00:01] "GET /index.html HTTP/1.1" 200
10.0.0.5 - - [04/Oct/2026:10:00:02] "GET /login HTTP/1.1" 200
192.168.1.10 - - [04/Oct/2026:10:00:03] "GET /api HTTP/1.1" 500
192.168.1.20 - - [04/Oct/2026:10:00:04] "GET /home HTTP/1.1" 200

The IP address is the first field.

We can use:

from collections import Counter

ip_counts = Counter()

with open("access.log", "r") as file:

    for line in file:

        parts = line.split()

        if parts:
            ip = parts[0]
            ip_counts[ip] += 1


for ip, count in ip_counts.most_common(10):
    print(f"{ip}: {count}")

Output:

192.168.1.10: 15230
192.168.1.20: 12045
10.0.0.5: 9321
...
7. What if the log format isn't predictable?

This is where regex becomes useful.

Suppose you need to find IP addresses anywhere in a line.

import re
from collections import Counter

ip_pattern = re.compile(
    r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
)

ip_counts = Counter()

with open("access.log", "r") as file:

    for line in file:

        ips = ip_pattern.findall(line)

        for ip in ips:
            ip_counts[ip] += 1


for ip, count in ip_counts.most_common(10):
    print(f"{ip}: {count}")
8. Why compile the regex?

Instead of repeatedly doing:

re.findall(pattern, line)

you can do:

pattern = re.compile(pattern)

once:

ip_pattern = re.compile(...)

and then:

ip_pattern.findall(line)

For a large log file, this is cleaner and avoids repeatedly compiling the same pattern.

9. A better production-style solution

For an interview, I'd write something like this:

import re
from collections import Counter

IP_PATTERN = re.compile(
    r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
)


def top_ips(log_file, limit=10):

    ip_counts = Counter()

    try:
        with open(log_file, "r") as file:

            for line in file:

                for ip in IP_PATTERN.findall(line):
                    ip_counts[ip] += 1

    except FileNotFoundError:
        print(f"Log file not found: {log_file}")
        return

    except PermissionError:
        print(f"Permission denied: {log_file}")
        return

    for ip, count in ip_counts.most_common(limit):
        print(f"{ip}: {count}")


top_ips("access.log")

This demonstrates several Python concepts at once:

function
   ↓
file handling
   ↓
exception handling
   ↓
regex
   ↓
Counter
   ↓
top N results

That's a nice interview solution.

10. Even better: command-line argument

For DevOps, don't hardcode:

top_ips("access.log")

You could accept the log file from the command line.

import sys

log_file = sys.argv[1]

top_ips(log_file)

Run:

python log_parser.py access.log

This is much more practical for automation.

Even better, you can use argparse:

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "log_file",
    help="Path to log file"
)

parser.add_argument(
    "--limit",
    type=int,
    default=10
)

args = parser.parse_args()

top_ips(args.log_file, args.limit)

Then:

python log_parser.py access.log --limit 10
11. Interview question: "Why Counter?"

Answer:

"Counter is designed for frequency counting. It provides a clean way to count occurrences and has most_common() built in, which makes it particularly useful for finding the top N errors or IP addresses."

12. Interview question: "What is the complexity?"

Suppose the log has N lines.

For the basic IP-counting solution:

Time:  O(N)

because you process each line once.

The dictionary/Counter stores the unique IPs.

If there are U unique IP addresses:

Space: O(U)

This is a good interview answer.

13. "Can you make it memory efficient?"

This is a common follow-up.

Say:

"Yes. I would process the file line by line instead of loading it entirely into memory. The log processing itself is streaming. The Counter still stores the unique keys, so memory depends on the number of unique IPs or error types rather than the total file size."

That's a strong answer.

14. One subtle point: invalid IP addresses

The regex:

r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

can match something like:

999.999.999.999

even though it's not a valid IPv4 address.

If the interviewer asks about production robustness, you can use Python's ipaddress module:

import ipaddress

try:
    ipaddress.ip_address(ip)
    ip_counts[ip] += 1
except ValueError:
    pass

You don't necessarily need this in the first solution unless validation is required.

15. What I'd actually write in an interview

If they ask:

"Find the top 10 IPs in a log file."

I'd start simple:

from collections import Counter

def top_ips(filename, n=10):

    counts = Counter()

    with open(filename) as file:

        for line in file:

            parts = line.split()

            if parts:
                ip = parts[0]
                counts[ip] += 1

    return counts.most_common(n)


for ip, count in top_ips("access.log"):
    print(f"{ip}: {count}")

Then I'd explain:

"I'm processing the file line by line so I don't load the entire log into memory. I'm using Counter to maintain frequencies and most_common(10) to get the top 10. This is O(N) for N log lines, with memory proportional to the number of unique IPs."

That's exactly the kind of answer I'd aim for in a Python DevOps interview.

16. What the interviewer is really testing

They aren't just testing whether you know regex.

They're looking for:

             Log Parsing
                 │
      ┌──────────┼───────────┐
      ↓          ↓           ↓
 File I/O    Data parsing   Counting
      │          │           │
      ↓          ↓           ↓
with open    split/regex   Counter
      │
      ↓
Large files?
      │
      ↓
stream line-by-line
      │
      ↓
Errors?
      │
      ↓
try/except
⭐ Memorize these points
Use with open() for safe file handling.
Process line by line for large logs.
Use split() when the format is simple and predictable.
Use regex when the format is more flexible.
Use Counter for frequency counting.
Use most_common(10) for top-N results.
Handle FileNotFoundError / PermissionError.
Know the complexity: roughly O(N) time and O(U) space for U unique keys.
For production DevOps scripts, consider command-line arguments rather than hardcoding filenames.
For real logs, be aware of log rotation, compressed .gz files, malformed lines, and very large numbers of unique keys.