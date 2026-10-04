```
•How do you check connectivity (ping, traceroute, curl, nc, telnet)?

For a DevOps interview, don't just memorize ping, curl, nc, and traceroute. Understand what layer each tool tests and when you'd use it during production troubleshooting.

🧠 First remember
ping       → Can I reach the host?
traceroute → Where is the network path failing/slow?
nc         → Can I connect to this specific TCP/UDP port?
telnet     → Can I establish a TCP connection to this port?
curl       → Does the HTTP/HTTPS service actually respond?

A very common troubleshooting flow is:

Application can't connect
        ↓
Can I reach the host?
        ↓
      ping
        ↓
Can I reach the port?
        ↓
      nc
        ↓
Does the HTTP service respond correctly?
        ↓
      curl
1. ping — Check basic host reachability

Example:

ping 8.8.8.8

or:

ping server.example.com

It uses ICMP Echo Request/Reply.

Example output:

64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=20.3 ms

You can learn:

whether ICMP replies are coming back
approximate round-trip latency
packet loss
DevOps scenario

Your application server can't reach a database server.

Start with:

ping db-server

If it works, you know there is at least some IP-level reachability.

⚠️ Interview trap

Ping failing does NOT necessarily mean the server is unreachable.

ICMP may be blocked by:

firewall
security group
network ACL
server configuration

For example:

ping → ❌
TCP 443 → ✅

The web service can still be completely reachable.

So don't say:

"Ping failed, therefore the server is down."

Say:

"Ping failure can indicate a connectivity problem, but ICMP may also be intentionally blocked."

2. traceroute — Find the network path

traceroute shows the path packets take toward a destination.

traceroute google.com

On some Linux systems you may also use:

tracepath google.com

Conceptually:

Your server
    ↓
Router 1
    ↓
Router 2
    ↓
Router 3
    ↓
Destination

Example:

1   10.0.0.1
2   10.20.0.1
3   172.16.0.1
4   ...
5   destination
DevOps scenario

Users report:

"The application is very slow."

You can use:

traceroute api.example.com

to investigate where latency may be appearing along the route.

Important interview point

A * * * at one hop does not automatically mean that hop is broken.

Some routers/firewalls simply don't respond to traceroute probes while forwarding traffic normally.

3. nc — Netcat ⭐

nc is extremely useful in DevOps.

It can test whether a specific TCP/UDP port is reachable.

For example:

nc -vz database.example.com 5432

Breakdown:

-v → verbose
-z → scan/check without sending application data

If successful:

Connection to database.example.com 5432 port [tcp/postgresql] succeeded!

Now you know:

Host reachable at TCP level
        +
Port 5432 reachable

This is much more useful than ping when troubleshooting an application connection.

4. Example: Database connectivity

Suppose your application says:

Connection refused

The database is supposed to listen on:

5432

You can test:

nc -vz db-server 5432

Possible results:

Connection succeeds
succeeded

Then the network path and TCP port are reachable.

The problem might instead be:

credentials
database authentication
application configuration
database protocol/application behavior
Connection refused
Connection refused

This commonly means you reached the host but nothing is accepting the connection on that port, or a device actively rejected it.

Investigate:

ss -lntp | grep 5432

on the database server.

Timeout
timed out

Potential causes include:

firewall
security group
routing problem
network ACL
service unreachable

Don't assume one cause without further testing.

5. telnet — Test TCP connectivity

You may see:

telnet database.example.com 5432

If it connects:

Connected to database.example.com.

That confirms a TCP connection was established.

However:

Telnet is generally not the preferred modern troubleshooting tool.

nc is usually more convenient.

So in an interview:

"telnet can test TCP connectivity to a port, but I generally prefer nc for this purpose."

6. curl — Test HTTP/HTTPS ⭐

This is one of the most important DevOps commands.

Suppose your API runs on:

http://10.0.0.10:8080

Run:

curl http://10.0.0.10:8080

You aren't just testing network connectivity—you are testing whether the HTTP service responds.

For headers:

curl -I https://example.com

For verbose troubleshooting:

curl -v https://example.com

For HTTP status only:

curl -o /dev/null -s -w "%{http_code}\n" https://example.com

You might get:

200
7. Why curl is different from ping

Suppose:

ping api.example.com

works.

That tells you:

ICMP connectivity works

But the application could still be broken.

For example:

curl https://api.example.com

might return:

HTTP/1.1 503 Service Unavailable

Now you know:

Network → reachable
TCP → reachable
HTTP → responding
Application/service → unhealthy

That's much more useful for troubleshooting an HTTP application.

8. curl with a specific port

You can test:

curl http://localhost:8080

This is very useful when debugging a service locally.

For example:

ss -lntp | grep 8080

shows:

LISTEN ... 0.0.0.0:8080

Then:

curl http://localhost:8080

tests whether the application actually responds.

9. A real DevOps troubleshooting scenario ⭐

Imagine:

Users can't access your web application.

You SSH into the application server.

Step 1 — Is the remote host reachable?
ping database-server

If ping fails, investigate networking—but remember ICMP may be blocked.

Step 2 — Is the required port reachable?

Database:

nc -vz database-server 5432

Web server:

nc -vz api-server 443
Step 3 — Does HTTP actually work?
curl -v https://api.example.com

Suppose you get:

HTTP/1.1 502 Bad Gateway

Now you know:

DNS/network/TCP may be working
        ↓
HTTP request reached a server/proxy
        ↓
But upstream application is failing

Now you'd investigate:

systemctl status myapp
journalctl -u myapp

This is where your earlier systemd knowledge connects directly.

10. Comparison table
Command	Primarily tests	Example
ping	ICMP/IP reachability	ping 10.0.0.10
traceroute	Network path/hops	traceroute example.com
nc	TCP/UDP port connectivity	nc -vz host 443
telnet	TCP connection	telnet host 443
curl	HTTP/HTTPS/application endpoint	curl -v https://example.com
11. How I'd troubleshoot "Connection refused"

This is a great interview scenario.

Suppose:

Application → Database
          ❌ Connection refused

I'd approach it systematically:

1. DNS
   ↓
   getent hosts db.example.com

2. Basic reachability
   ↓
   ping db.example.com

3. TCP port
   ↓
   nc -vz db.example.com 5432

4. On database server
   ↓
   ss -lntp | grep 5432

5. Firewall/security group
   ↓
   Check network controls

6. Application configuration
   ↓
   Check host/port/credentials

For HTTP:

curl -v https://api.example.com

can give you much more information than ping.

⭐ Interview answer to memorize

If asked:

"How do you check connectivity in Linux?"

Say:

"It depends on what I'm trying to test. I use ping to test basic ICMP reachability, traceroute to investigate the network path, nc to test connectivity to a specific TCP or UDP port, and curl to test an HTTP or HTTPS service at the application layer. telnet can also test TCP connectivity, although I generally prefer nc. I don't rely only on ping because ICMP can be blocked even when the actual application is reachable."

🧠 Best memory trick
ping
 ↓
Can I reach the host?

traceroute
 ↓
Where does the path go?

nc
 ↓
Can I reach the port?

curl
 ↓
Does the application respond?

telnet
 ↓
Can I establish TCP?

The key DevOps mindset: don't just ask "Is the server reachable?" Ask which layer is failing: DNS → routing/IP → TCP port → TLS → HTTP → application.