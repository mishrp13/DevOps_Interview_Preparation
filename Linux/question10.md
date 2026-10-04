```
•How do you find which process is using a port? (ss -tulnp, lsof -i)

For a DevOps interview, this is a very practical Linux troubleshooting question.

A common scenario is:

"Your application is trying to start on port 8080, but you get Address already in use. How do you find which process is using port 8080?"

Two important commands are:

ss -tulnp

and

lsof -i
1. Using ss
Find all listening ports
ss -tulnp

Let's break it down:

-t  → TCP
-u  → UDP
-l  → listening sockets
-n  → don't resolve names; show numeric ports
-p  → show process information

So:

ss -tulnp

means roughly:

"Show TCP/UDP listening ports and tell me which process owns them."

You might see:

Netid  State   Local Address:Port   Process
tcp    LISTEN  0.0.0.0:22          users:(("sshd",pid=721,fd=3))
tcp    LISTEN  0.0.0.0:80          users:(("nginx",pid=1050,fd=6))
tcp    LISTEN  0.0.0.0:8080        users:(("python",pid=2345,fd=3))

Now you know:

Port 8080
   ↓
PID 2345
   ↓
python

You can then investigate:

ps -p 2345 -f
2. Find a specific port

Instead of looking through everything:

ss -tulnp | grep :8080

Example:

tcp LISTEN 0 128 0.0.0.0:8080 0.0.0.0:* users:(("java",pid=4567,fd=123))

Now:

Port → 8080
Process → java
PID → 4567

You can inspect it:

ps -p 4567 -f
3. Using lsof

Another very useful command is:

lsof -i :8080

This asks:

"Which process has port 8080 open?"

Example:

COMMAND  PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
java     4567  app    123u IPv4  ...    TCP *:8080 (LISTEN)

From this you can identify:

COMMAND → java
PID     → 4567
PORT    → 8080

Then:

ps -p 4567 -f
4. ss vs lsof
Command	Useful for
ss -tulnp	Quickly inspect network sockets/listening ports
ss -tulnp | grep :8080	Find what's listening on a specific port
lsof -i :8080	Directly identify the process using a specific port
ps -p PID -f	Get detailed process information

A good DevOps engineer should be comfortable with both.

5. Real DevOps troubleshooting scenario ⭐

Suppose you deploy an application:

./start-app.sh

You get:

Error: Address already in use

You know your application should use:

8080
Step 1 — Find who owns the port
ss -tulnp | grep :8080

Suppose you get:

tcp LISTEN 0 128 0.0.0.0:8080 0.0.0.0:* users:(("java",pid=4567,fd=123))
Step 2 — Investigate the process
ps -p 4567 -f

Maybe:

UID   PID   PPID  CMD
app   4567  1     java -jar old-app.jar

Now you know an old application instance is occupying port 8080.

Step 3 — Decide what to do

You might gracefully stop it:

kill -15 4567

Then verify:

ss -tulnp | grep :8080

If the process is still stuck, you could investigate further and potentially use:

kill -9 4567

as a last resort.

6. Another useful command

You may also hear:

netstat -tulnp

Historically, netstat was commonly used for this.

For example:

netstat -tulnp | grep :8080

But on many modern Linux systems, ss is preferred.

So in an interview, I'd lead with:

ss -tulnp

and mention:

lsof -i :8080

as another option.

⭐ Interview answer

If the interviewer asks:

"How do you find which process is using port 8080?"

A strong answer is:

"I can use ss -tulnp | grep :8080 to see which process is listening on port 8080. It gives me the process name and PID. Alternatively, I can use lsof -i :8080. Once I have the PID, I can use ps -p <PID> -f to inspect the process."

For example:

ss -tulnp | grep :8080
tcp LISTEN ... users:(("java",pid=4567,...))

Then:

ps -p 4567 -f
🧠 Remember this troubleshooting chain
Port problem
     ↓
ss -tulnp | grep :8080
     ↓
Find PID
     ↓
ps -p <PID> -f
     ↓
Understand process
     ↓
Decide whether/how to stop it

This is exactly the kind of real-world troubleshooting flow interviewers often want rather than just memorizing the commands.