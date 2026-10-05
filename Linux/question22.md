```
•What is the difference between TCP and UDP?


For a DevOps interview, don't just say “TCP is reliable and UDP is faster.” Explain how that affects applications, ports, load balancers, Kubernetes, troubleshooting, and AWS.

1. TCP vs UDP — the core difference

| TCP                             | UDP                                     |
| ------------------------------- | --------------------------------------- |
| Connection-oriented             | Connectionless                          |
| Reliable delivery               | No delivery guarantee                   |
| Ordered data                    | No ordering guarantee                   |
| Retransmits lost packets        | Doesn't retransmit                      |
| Uses acknowledgments            | No TCP-style ACK                        |
| Flow/congestion control         | No built-in TCP-style flow control      |
| More overhead                   | Lower overhead                          |
| Generally higher latency        | Generally lower latency                 |
| HTTP/HTTPS, SSH, DB connections | DNS, DHCP, streaming, VoIP, QUIC/HTTP/3 |

Interview one-liner

“TCP provides a reliable, ordered, connection-oriented byte stream, while UDP is connectionless and sends datagrams without guaranteeing delivery or ordering.”

2. How TCP works

Suppose your application connects to:

server:443

TCP first establishes a connection using the three-way handshake:

Client                    Server

   SYN  ──────────────────►
        ◄────────────────── SYN-ACK
   ACK  ──────────────────►

       Connection established

Then data is transferred.

If a packet is lost:

Client                    Server

Packet 1 ────────────────►
Packet 2 ────────────────►
Packet 3 ───────X

             missing packet detected
             
Packet 3 ◄──────────────── retransmission

TCP handles things like:

acknowledgments
sequence numbers
retransmissions
ordering
flow control
congestion control

So the application doesn't have to implement all of that itself.

3. How UDP works

UDP doesn't establish a TCP-style connection first.

Conceptually:

Client                    Server

Packet 1 ────────────────►
Packet 2 ────────────────►
Packet 3 ───────X

Packet 4 ────────────────►

UDP essentially says:

“Here's my datagram. Do what you can with it.”

If packet 3 disappears, UDP itself doesn't retransmit it.

That can be desirable when speed and low overhead matter more than guaranteed delivery.

4. TCP is a byte stream

This is a subtle point that can impress an interviewer.

TCP doesn't preserve application-level message boundaries.

If an application sends:

HELLO
WORLD

TCP provides a reliable ordered byte stream.

The receiver might read:

HELLOWORLD

or chunks such as:

HEL
LOWO
RLD

The application protocol has to define its own message framing.

UDP, on the other hand, preserves datagram boundaries.

5. Real DevOps examples
TCP

You'll commonly encounter TCP with:

HTTPS       → 443
HTTP        → 80
SSH         → 22
PostgreSQL  → 5432
MySQL       → 3306
Redis       → 6379

For example:

Application
     │
     │ TCP
     ▼
PostgreSQL :5432

You care about reliable delivery because losing or reordering database traffic would be unacceptable.

UDP

Common examples include:

DNS      → 53/UDP
DHCP     → 67/68 UDP
NTP      → 123/UDP
VoIP
Streaming
Some gaming traffic

DNS is a particularly useful DevOps example.

A normal DNS query can use UDP because the request/response is small and avoiding TCP connection setup is efficient.

6. Important: DNS can use TCP too

Don't say:

“DNS always uses UDP.”

That's incorrect.

DNS traditionally uses UDP for many queries, but TCP is also used, including for cases such as larger responses and zone transfers.

Modern DNS can also use other transports in some scenarios.

A safe interview answer is:

“DNS commonly uses UDP for normal queries, but DNS can also use TCP when required.”

7. HTTP/HTTPS and TCP

Traditional HTTP/1.1 and HTTP/2 commonly run over TCP:

HTTP
  ↓
TCP
  ↓
IP
  ↓
Ethernet/Wi-Fi

For HTTPS:

HTTPS
  ↓
TLS
  ↓
TCP
  ↓
IP

For example:

Browser
   │
   ▼
TCP connection
   │
   ▼
Load Balancer :443
   │
   ▼
Application
8. Important modern exception: HTTP/3

This is a good advanced DevOps interview point.

HTTP/3 uses:

HTTP/3
   ↓
QUIC
   ↓
UDP
   ↓
IP

QUIC implements reliability, encryption, streams, etc. at a higher layer while using UDP as its transport foundation.

So don't say:

“HTTPS always uses TCP.”

A better answer is:

“HTTP/1.1 and HTTP/2 commonly run over TCP, while HTTP/3 uses QUIC over UDP.”

That shows modern networking knowledge.

9. DevOps troubleshooting scenario

Interviewer:

“Your application is running on port 8080, but clients can't connect. What would you check?”

I'd say:

First check whether the application is listening:
ss -ltnp | grep :8080

You might see:

LISTEN 0 128 0.0.0.0:8080

Then determine the protocol.

If it's TCP:

Client
  │
  ▼
TCP :8080
  │
  ▼
Firewall / Security Group
  │
  ▼
Application

I'd check:

application binding address
port
Linux firewall
AWS Security Group
NACL
route table
load balancer
container port mapping
Kubernetes Service/NetworkPolicy
10. TCP connection states

As a DevOps engineer, you should recognize:

LISTEN
SYN-SENT
SYN-RECEIVED
ESTABLISHED
FIN-WAIT
TIME-WAIT
CLOSE-WAIT

Check them with:

ss -tan

For example:

ESTABLISHED

means a TCP connection is established.

11. TIME_WAIT — common interview follow-up

Interviewer might ask:

“Why do I see lots of TIME_WAIT connections?”

TCP needs to ensure delayed packets from an old connection don't interfere with a new connection using the same connection tuple.

You can inspect:

ss -tan state time-wait

A large number isn't automatically a problem. You need to understand the traffic pattern and whether there are resource/port exhaustion symptoms.

12. CLOSE_WAIT vs TIME_WAIT

Another good DevOps question.

TIME_WAIT

Usually indicates the local side has actively closed a TCP connection and is waiting for enough time to ensure delayed packets don't cause problems.

CLOSE_WAIT

Usually means:

The remote side closed its connection, but the local application hasn't closed its side yet.

If you see a large and continually growing number of CLOSE_WAIT connections, it can indicate an application bug where connections aren't being closed properly.

This is much more interesting from a troubleshooting perspective.

13. TCP vs UDP in Kubernetes

Kubernetes Services can expose both TCP and UDP.

Example:

ports:
  - port: 8080
    targetPort: 8080
    protocol: TCP

For a UDP service:

ports:
  - port: 53
    targetPort: 53
    protocol: UDP

So when troubleshooting a Kubernetes service, you need to know:

Service port
    ↓
Target port
    ↓
Protocol
    ↓
Pod

A TCP service configuration won't magically make a UDP application work.

14. TCP vs UDP in AWS

This becomes important with Security Groups.

A security group rule specifies the protocol.

For example:

TCP 443

allows TCP traffic on port 443.

Whereas:

UDP 53

allows UDP traffic on port 53.

So if your application uses UDP but you only allow TCP:

Client
   │
   │ UDP
   ▼
Security Group
   │
   X

the traffic won't work.

15. When would you choose TCP vs UDP?
Choose TCP when:

You need:

reliable delivery
ordered data
retransmission
connection semantics

Examples:

HTTPS
SSH
Database connections
Git over SSH/HTTPS
Choose UDP when:

You care about:

low overhead
low latency
application-controlled reliability
real-time traffic

Examples:

DNS
VoIP
Some streaming
Gaming
QUIC/HTTP/3
16. A strong interview answer

If the interviewer asks:

“What's the difference between TCP and UDP?”

I'd answer:

“TCP is connection-oriented and provides reliable, ordered delivery using mechanisms such as sequence numbers, acknowledgments, retransmissions, flow control and congestion control. UDP is connectionless and provides datagrams without guaranteeing delivery or ordering, so it has lower protocol overhead. In DevOps, I commonly see TCP with HTTPS, SSH and database connections, while UDP is common with DNS, NTP and real-time traffic. One modern exception is HTTP/3, which uses QUIC over UDP.”

Then add:

“When troubleshooting, I first identify whether the application expects TCP or UDP, then verify the listening socket with ss, and check firewalls, AWS Security Groups, load balancers, Kubernetes Services and NetworkPolicies accordingly.”

⭐ Memorize this
TCP
├── Connection-oriented
├── Reliable
├── Ordered
├── Retransmission
├── Flow/congestion control
└── HTTPS / SSH / DB

UDP
├── Connectionless
├── No delivery guarantee
├── No ordering guarantee
├── Lower overhead
└── DNS / NTP / real-time / QUIC

Interview golden line:

“TCP gives the application a reliable ordered byte stream; UDP gives it lightweight datagrams and leaves reliability and ordering, if needed, to the application or a higher-level protocol.”