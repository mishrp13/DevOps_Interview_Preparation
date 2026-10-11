```
•grep, awk, sed, cut, sort | uniq -c, xargs, find

Linux commands for a DevOps interview
These commands are essential for Linux troubleshooting, log analysis, automation, and CI/CD pipelines. In interviews, you should know what each command does, its syntax, and one real-world DevOps example.

1. Quick cheat sheet


Command                        Purpose                           DevOps Use Case
grep                           Search text by pattern            Find errors in application logs
awk                            Extract and process columns       Analyze access logs and metrics
sed                            Replace or edit text               Update configuration values
cut                            Extract fields or columns         Extract usernames, IPs, or CSV columns
sort                             Sort lines                        Sort IP addresses or log entries
uniq -c                     Count consecutive duplicate lines   Count repeated errors or IPs
xargs                      Pass input as command arguments    Process files or terminate selected processes
find                       Search files and directories            Locate old logs and large files

2. grep — Search for matching text

Interview definition: grep searches files or command output for lines matching a pattern.
Basic syntax:
grep "ERROR" app.log


Prints every line containing ERROR.


Useful examples:
# Case-insensitive search
grep -i "error" app.log

# Show line numbers
grep -n "ERROR" app.log

# Search recursively in a directory
grep -r "connection refused" /var/log/

# Show lines that do NOT match
grep -v "INFO" app.log

# Count matching lines
grep -c "ERROR" app.log

Real DevOps scenario: An application is failing after deployment. Search the logs for errors:
grep -i "error\|exception\|failed" app.log

This searches for any of the three patterns using basic regular-expression alternation.

3.

awk — Extract columns and process text

Interview definition: awk is a text-processing tool that reads input line by line and works with fields or columns.

Basic syntax:
awk '{print $1}' file.txt

$1 is the first field, $2 is the second field, and $0 is the entire line.

Example input, access.log:
192.168.1.10 GET /home 200
192.168.1.20 POST /login 500
192.168.1.10 GET /about 200


Examples:
# Print the first column (IP address)
awk '{print $1}' access.log

# Print IP and HTTP status
awk '{print $1, $4}' access.log

# Count requests returning status 500
awk '$4 == 500 {count++} END {print count+0}' access.log

For comma-separated data:
awk -F',' '{print $1}' users.csv


-F',' sets the field separator to a comma.

Real DevOps scenario: Extract IP addresses from web logs, count HTTP status codes, or calculate metrics from structured text.


4. 

sed — Replace or edit text
Interview definition: sed is a stream editor used to search, replace, delete, or transform text.
Basic syntax:
sed 's/old/new/' file.txt


This replaces the first occurrence of old with new on each line and prints the result. It does not modify the original file.

Examples:
# Replace the first occurrence on each line
sed 's/dev/prod/' config.txt

# Replace all occurrences on each line
sed 's/dev/prod/g' config.txt

# Print lines containing ERROR
sed -n '/ERROR/p' app.log

# Delete blank lines from output
sed '/^$/d' config.txt


To modify a file directly on GNU/Linux:
sed -i 's/DEBUG=false/DEBUG=true/' config.env


Be careful with in-place edits, especially in production configuration files. Back up important files first.
Real DevOps scenario: Update a configuration value during deployment or remove unwanted lines from a file.


5.

cut — Extract specific fields
Interview definition: cut extracts selected character positions or delimited fields from each line.

Examples:
# Extract the first colon-separated field
cut -d':' -f1 /etc/passwd

# Extract the first and third CSV fields
cut -d',' -f1,3 users.csv

# Extract characters 1 through 5
cut -c1-5 file.txt


Here:
- -d specifies the delimiter.
- -f specifies field numbers.
- -c specifies character positions.
Real DevOps scenario: Extract usernames from /etc/passwd, or extract particular columns from simple CSV files.
Interview follow-up: cut is suitable for simple, consistently delimited text. For more complex field processing, awk is more flexible.

6.

sort | uniq -c — Count repeated values
These commands are commonly used together in log analysis.
Interview definition:
- sort arranges lines in sorted order.
- uniq -c counts consecutive identical lines.
Example:
sort names.txt | uniq -c


Input:
alice
bob
alice
alice
bob


Output:
      3 alice
      2 bob


Why use sort first? Because uniq counts only adjacent duplicate lines. Sorting brings identical lines together.
Real DevOps example: Find the most frequent IP addresses
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -10


What each part does:
1. awk '{print $1}' extracts IP addresses.
2. sort groups identical addresses together.
3. uniq -c counts each address.
4. sort -nr sorts counts numerically in descending order.
5. head -10 prints the top 10.


This is useful for finding high-volume clients or investigating unusual traffic. Frequent requests alone do not prove malicious activity.


7.

xargs — Convert input into command arguments
Interview definition: xargs reads items from standard input and passes them as arguments to another command.
Example:
cat files.txt | xargs ls -l


This runs ls -l with the filenames from the input.
More practical examples:
# Search for ERROR in a list of files
cat files.txt | xargs grep -n "ERROR"

# Pass filenames safely using null delimiters
find /tmp -type f -name '*.tmp' -print0 | xargs -0 ls -l


The second example uses -print0 and -0 to handle filenames containing spaces or newline characters safely.
Real DevOps scenario: Process batches of log files, run commands on discovered files, or automate repetitive tasks.

Be careful with destructive commands such as rm. Always inspect the target list before deleting files.

8.

find — Search files and directories
Interview definition: find searches a directory tree based on criteria such as filename, type, modification time, and size.
Examples:
# Find files named app.log
find /var/log -type f -name "app.log"

# Find all .log files
find /var/log -type f -name "*.log"

# Find files larger than 100 MB
find /var/log -type f -size +100M

# Find files modified more than 7 days ago
find /var/log -type f -mtime +7

# Find directories named cache
find /opt -type d -name "cache"


Real DevOps scenario: Identify old log files
find /var/log/myapp -type f -name "*.log" -mtime +7


This lists matching log files last modified more than seven 24-hour periods ago.

To delete those files, you could use:
find /var/log/myapp -type f -name "*.log" -mtime +7 -print


First inspect the output. Once you verify the targets, you can add -delete if deletion is intended and permitted.

9.

Real interview task: Combine the commands
Question: Find the top 5 most common errors in an application log.
grep "ERROR" app.log | sort | uniq -c | sort -nr | head -5

Pipeline explanation:
grep "ERROR" app.log
Filter error lines

sort | uniq -c
Group identical lines and count them

sort -nr | head -5
Display the five most frequent lines


Note: This counts identical full error lines. If log messages include different timestamps, you may need to normalize or extract the error message first.



