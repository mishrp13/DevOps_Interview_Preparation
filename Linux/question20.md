```
•netstat vs ss?

For a DevOps interview, don't just say "ss is newer than netstat." Explain what problem they solve, the commands you actually use, and why ss is preferred in modern Linux environments.

1. What are netstat and ss?

Both are Linux networking tools used to inspect:

Listening ports
Established connections
TCP/UDP sockets
Local/remote IP addresses
Connection states
Sometimes process/PID information

The main difference:

|                        | `netstat`            | `ss`                  |
| ---------------------- | -------------------- | --------------------- |
| Full name              | Network Statistics   | Socket Statistics     |
| Status                 | Older/legacy         | Modern                |
| Speed                  | Generally slower     | Generally faster      |
| Modern Linux           | May not be installed | Usually available     |
| Socket information     | Yes                  | Yes, more extensively |
| Typical recommendation | Legacy systems       | **Preferred**         |

Interview answer

“netstat and ss are both used to inspect network connections and listening ports. netstat is the older utility from the net-tools package, while ss is the modern socket-statistics utility and is generally preferred because it's faster and provides more detailed socket information.”

2. Most important DevOps commands

Suppose your application should be listening on port 8080.

Using netstat
netstat -tulnp
Using ss
ss -tulnp

Both show listening TCP/UDP ports and associated processes when permissions allow.

You'll see something conceptually like:

Proto  Local Address      State       PID/Program
tcp    0.0.0.0:8080       LISTEN      1234/java

This immediately answers:

“Is my application actually listening on port 8080?”

3. Break down ss -tulnp

This is a command worth memorizing for interviews:

ss -tulnp

Meaning:

-t → TCP
-u → UDP
-l → Listening
-n → Don't resolve DNS/service names
-p → Show process/PID

So:

“Show me TCP and UDP listening sockets, use numeric addresses/ports, and show the owning process.”

4. Find who is listening on port 8080

This is probably the most useful DevOps troubleshooting command:

ss -ltnp | grep :8080

Breakdown:

-l → listening
-t → TCP
-n → numeric
-p → process

Example:

LISTEN 0 128 0.0.0.0:8080 0.0.0.0:* users:(("java",pid=1234,fd=123))

You can say:

“If an application isn't reachable, I first check whether the process is actually listening on the expected port.”

5. Check established connections
ss -tn

Or:

netstat -tn

You'll see states such as:

ESTAB
TIME-WAIT
CLOSE-WAIT
LISTEN
SYN-SENT
SYN-RECV

For example:

ss -tan

shows TCP sockets, including listening and non-listening sockets.

6. ss can filter connections

This is where ss becomes really useful.

Show connections to port 443
ss -tn dst :443
Show connections from port 8080
ss -tn sport :8080
Show listening TCP sockets on port 8080
ss -ltn 'sport = :8080'

You don't need to memorize every filter syntax for an interview, but knowing that ss supports powerful filtering is useful.

7. netstat equivalent commands
Requirement	netstat	ss
Listening ports	netstat -tulnp	ss -tulnp
TCP connections	netstat -tn	ss -tn
All TCP connections	netstat -ant	ss -ant
Routing table	netstat -rn	ip route
Interface statistics	netstat -i	ip -s link

Notice something interesting:

For modern Linux, you should also know the ip command.

For example:

ip addr
ip route
ip link

So don't present netstat as your primary networking tool in a modern DevOps interview.

8. Why is ss faster?

This is a nice interview follow-up.

ss obtains socket information directly through modern Linux kernel interfaces such as netlink, whereas the older netstat approach relies on /proc-based information and the legacy net-tools stack.

You don't need to go deeply into kernel internals unless asked.

A good answer is:

“ss is designed for efficient socket inspection and uses modern kernel interfaces, so it's generally faster and more capable than the legacy netstat utility, especially on systems with many connections.”

9. Real DevOps troubleshooting scenario

Interviewer:

“My application is running but users can't access it on port 8080. What do you check?”

A strong answer:

Step 1 — Is the process running?
ps aux | grep java

or:

systemctl status myapp
Step 2 — Is it listening?
ss -ltnp | grep :8080

If nothing appears:

Application isn't listening on 8080

Investigate application configuration/logs.

If you see:

0.0.0.0:8080

the application is listening on all IPv4 interfaces.

If you see:

127.0.0.1:8080

that's interesting.

The application is only listening on localhost.

A remote client won't normally be able to connect directly.

10. Then check firewall/networking

If the application is listening:

ss -ltnp | grep :8080

but users still can't connect, I'd investigate:

Application
    ↓
Linux socket
    ↓
Host firewall
    ↓
Security Group
    ↓
NACL / routing
    ↓
Load Balancer
    ↓
Client

For AWS, I'd check:

Security Groups
Network ACLs
Route tables
Load balancer target health
Application binding address
Container port mapping

This is where the question becomes DevOps, rather than simply Linux commands.

11. 0.0.0.0 vs 127.0.0.1

This is another common interview question.

Suppose:

ss -ltnp

shows:

127.0.0.1:8080

It means the application is bound to the loopback interface.

If it shows:

0.0.0.0:8080

it means it's listening on all IPv4 interfaces.

Conceptually:

127.0.0.1
   │
   └── This machine only


0.0.0.0
   │
   └── All IPv4 interfaces

In containers, this distinction is especially important.

12. Docker example

Suppose your application listens inside a container:

0.0.0.0:8080

and Docker runs:

docker run -p 8080:8080 myapp

Then:

Client
  │
  ▼
Host :8080
  │
  ▼
Docker port mapping
  │
  ▼
Container :8080
  │
  ▼
Application

If the application inside the container binds only to:

127.0.0.1:8080

you can run into connectivity problems because it isn't listening on the container's network interface.

This is a very good DevOps interview connection.

13. What about UDP?

ss:

ss -lunp

means:

-l → listening
-u → UDP
-n → numeric
-p → process

For example, DNS commonly uses UDP port 53.

You can check:

ss -lunp | grep :53
14. What I'd say in the interview

If they ask:

“What's the difference between netstat and ss?”

Give this:

“Both are Linux networking utilities used to inspect sockets, listening ports and network connections. netstat is the older utility from the net-tools package, while ss is the modern replacement and is generally faster and more feature-rich. In modern DevOps troubleshooting, I normally use ss, for example ss -ltnp to identify TCP listening ports and the processes using them. I use netstat mainly when dealing with older systems where it's already installed.”

Then add:

“For troubleshooting an application, I'd use ss to verify whether the application is listening on the expected address and port, and then investigate firewall, security-group, load-balancer, routing or container networking issues if the socket is healthy but the application is still unreachable.”

That's a strong DevOps answer because you're showing that you understand not only the command but where it fits into an actual incident/debugging workflow.

⭐ Memorize these 5 commands
# 1. All listening TCP/UDP ports
ss -tulnp

# 2. All TCP connections
ss -tan

# 3. Listening TCP ports
ss -ltn

# 4. Who is using port 8080?
ss -ltnp | grep :8080

# 5. Routing table
ip route

Interview shortcut:
netstat = legacy
ss = modern socket troubleshooting
ip = modern interface/routing configuration