```
•How do you find the top 10 IPs in an access log using one command?


Interview question: How do you find the top 10 IP addresses that appear most frequently in a web server access log using one command?
1. Command to remember
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -10


This command extracts IP addresses, counts how often each appears, sorts them by frequency, and prints the top 10.
2. Understand each command
Let's say access.log contains:
192.168.1.10 GET /home 200
192.168.1.20 GET /login 200
192.168.1.10 GET /about 200
192.168.1.30 GET /home 500
192.168.1.10 GET /login 200
192.168.1.20 GET /home 200



Step 1: awk '{print $1}' access.log
Extracts the first column, which is the client IP address.
Output: one IP per line.




Step 2: sort
Sorts the IP addresses alphabetically so identical addresses are next to each other.




Step 3: uniq -c
Counts consecutive duplicate IP addresses.




Step 4: sort -nr
Sorts the counts numerically (-n) in reverse order (-r), highest first.




Step 5: head -10
Displays only the first 10 results.



3. Expected output
For the sample data above, the command produces:
      3 192.168.1.10
      2 192.168.1.20
      1 192.168.1.30


There are only three distinct IP addresses in this sample, so only three results appear.
4. How to explain it in the interview
“I use awk to extract the client IP from the first column. Then I sort the IPs so duplicates become adjacent, use uniq -c to count them, sort the counts numerically in descending order, and use head -10 to display the ten most frequent IP addresses. This is useful for web traffic analysis and troubleshooting suspicious traffic patterns.”

Important: This assumes the IP address is the first whitespace-separated field in the access log, as in common Nginx and Apache access-log formats. High request counts can indicate legitimate traffic as well as suspicious activity, so they should be investigated in context.