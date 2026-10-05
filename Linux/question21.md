```

•How does DNS resolution work? What is in /etc/resolv.conf and /etc/hosts?

This is a very common DevOps interview topic because DNS sits between the application and the network. A good answer should cover resolution flow + /etc/hosts + /etc/resolv.conf + troubleshooting.

1. What is DNS?

DNS = Domain Name System.

Its job is to translate a hostname into an IP address.

For example:

www.example.com
       ↓
   DNS lookup
       ↓
93.184.216.34

Your application generally doesn't want to remember IP addresses. It connects to a hostname, and DNS resolves that hostname to an address.

2. How DNS resolution works

Suppose you run:

curl https://api.example.com

Your machine needs to determine:

api.example.com → IP address

A simplified flow is:

Query · A www.example.com?
Client
Recursive resolver
Root
TLD (.com)
Authoritative
1
2
3
4
5
6
7
8
Query
The client asks its recursive resolver for A www.example.com.
Uncached
Cached
Uncached
Cached
Give feedback
Application
     │
     ▼
OS resolver
     │
     ├── /etc/hosts?
     │
     └── DNS resolver
             │
             ▼
        Recursive DNS server
             │
             ▼
           Root
             │
             ▼
       .com TLD server
             │
             ▼
     Authoritative DNS server
             │
             ▼
       IP address
             │
             ▼
        Application
Important interview point

The application usually doesn't directly ask the root DNS server.

It normally asks a configured recursive DNS resolver, which does the necessary DNS lookups on its behalf if the answer isn't already cached.

3. Step-by-step example

You execute:

ping api.example.com
Step 1 — Application asks the OS

The application uses the operating system's name-resolution mechanism.

The OS checks its configured resolution sources.

One important source is:

/etc/hosts

If the hostname is found there, DNS may not be needed.

Step 2 — If not found, ask DNS

The system uses its configured DNS resolver.

This information is commonly configured through:

/etc/resolv.conf

For example:

nameserver 8.8.8.8
nameserver 1.1.1.1

The machine can send a DNS query to one of those servers.

4. What is /etc/hosts?

/etc/hosts is a local hostname-to-IP mapping file.

Example:

127.0.0.1       localhost
192.168.1.10    webserver
192.168.1.20    database
10.0.0.50       api.internal

So if you run:

ping database

the system can resolve:

database → 192.168.1.20

without querying DNS, depending on the system's configured lookup order.

5. Why is /etc/hosts useful in DevOps?

Very useful for:

Local development
127.0.0.1 myapp.local
Testing

You can temporarily point:

api.example.com → test server

For example:

10.10.10.50 api.example.com

Then:

curl https://api.example.com

will resolve to that local mapping if /etc/hosts is consulted first.

Troubleshooting

You can test whether an application works against a particular IP without changing public DNS.

6. What is /etc/resolv.conf?

/etc/resolv.conf contains DNS resolver configuration.

Example:

search example.com
nameserver 10.0.0.2
nameserver 8.8.8.8
options timeout:2 attempts:3

Important directives:

nameserver
nameserver 10.0.0.2

Tells the system which DNS server(s) to query.

search
search example.com

Provides search domains for resolving short/unqualified names.

For example, depending on resolver behavior:

ping web

may try:

web.example.com
options

Controls resolver behavior such as timeout/retry settings.

7. /etc/hosts vs /etc/resolv.conf

This is an excellent interview comparison:

| `/etc/hosts`                           | `/etc/resolv.conf`                     |
| -------------------------------------- | -------------------------------------- |
| Local hostname mapping                 | DNS resolver configuration             |
| Maps hostname → IP                     | Specifies DNS servers/search options   |
| No DNS server required                 | Used to communicate with DNS resolvers |
| Manually/static managed in many setups | Often generated/managed automatically  |
| Useful for overrides/testing           | Used for normal DNS resolution         |


Think:

/etc/hosts
    ↓
"These names map to these IPs locally."


/etc/resolv.conf
    ↓
"Ask these DNS servers when you need DNS."
8. Very important: /etc/hosts does not always mean "DNS first"

A common interview trap is:

“Does Linux always check /etc/hosts before DNS?”

Don't simply say yes.

The lookup order is controlled by the system's Name Service Switch (NSS) configuration, commonly:

/etc/nsswitch.conf

Look at:

cat /etc/nsswitch.conf

You may see:

hosts: files dns

This means:

files → /etc/hosts
   ↓
dns → DNS

So /etc/hosts is consulted before DNS.

But the exact configuration can differ.

Interview-quality answer

“The lookup order isn't universally hardcoded. On Linux it's commonly controlled by NSS through /etc/nsswitch.conf. A common configuration is hosts: files dns, meaning /etc/hosts is checked before DNS.”

That's much better than saying "/etc/hosts is always checked first."

9. DNS record types you should know

For DevOps interviews, know at least these:

A

Hostname → IPv4

example.com → 10.10.10.10
AAAA

Hostname → IPv6

example.com → 2001:db8::1
CNAME

Alias → another hostname

www.example.com
       ↓
example.com
MX

Mail server information.

NS

Nameservers responsible for a DNS zone.

TXT

Text records, commonly used for things such as domain verification and email-related policies.

10. How would you troubleshoot DNS?

This is where the question becomes DevOps.

Suppose:

curl https://api.example.com

fails with:

Could not resolve host: api.example.com

I'd troubleshoot systematically.

Step 1 — Check /etc/hosts
cat /etc/hosts
Step 2 — Check resolver configuration
cat /etc/resolv.conf

Look for:

nameserver ...
Step 3 — Check NSS
cat /etc/nsswitch.conf

Look for:

hosts: files dns
Step 4 — Test DNS directly

Use:

dig api.example.com

or:

nslookup api.example.com
Step 5 — Test connectivity to the DNS server

For example:

ping <dns-server>

or investigate network/firewall configuration as appropriate.

11. dig is very useful in DevOps

For example:

dig example.com

You might see:

;; ANSWER SECTION:

example.com.    300    IN    A    93.184.216.34

You can specifically ask for an A record:

dig example.com A

CNAME:

dig www.example.com CNAME

Or query a specific DNS server:

dig @8.8.8.8 example.com

This is extremely useful for determining whether the problem is:

Application problem
       OR
DNS resolution problem
12. DevOps scenario: "It works by IP but not by hostname"

Suppose:

curl http://10.0.0.50:8080

works.

But:

curl http://api.internal:8080

fails.

That strongly suggests investigating DNS/name resolution.

I'd check:

getent hosts api.internal

Then:

cat /etc/hosts
cat /etc/resolv.conf
cat /etc/nsswitch.conf
dig api.internal

This is a very practical troubleshooting sequence.

13. Kubernetes connection — VERY important for DevOps

If you're interviewing for a Kubernetes role, mention this.

Inside Kubernetes, DNS is heavily used for service discovery.

For example:

my-service

can resolve to a Kubernetes Service IP.

A pod may have:

/etc/resolv.conf

containing a cluster DNS nameserver and search domains.

Conceptually:

Pod
 │
 ├── /etc/hosts
 │
 └── /etc/resolv.conf
          │
          ▼
    Kubernetes DNS
          │
          ▼
       Service
          │
          ▼
      Pod endpoints

So when debugging:

curl http://my-service:8080

and it fails, you might check:

cat /etc/resolv.conf
getent hosts my-service
nslookup my-service

This connects your Linux knowledge directly to Kubernetes troubleshooting.

14. Docker connection

Docker containers also have their own DNS configuration.

Inside a container:

cat /etc/resolv.conf

can help determine which DNS resolver the container is using.

A common troubleshooting flow:

Container
   │
   ▼
Can resolve hostname?
   │
   ├── NO → inspect DNS configuration
   │
   └── YES
        │
        ▼
   Can connect to IP?
        │
        ├── NO → network/firewall/routing
        │
        └── YES → investigate application
15. One subtle point about /etc/resolv.conf

In modern Linux systems, /etc/resolv.conf may not be a manually maintained file.

It can be generated or managed by components such as:

systemd-resolved
NetworkManager
DHCP/network configuration
container runtimes
Kubernetes

So don't casually say:

"/etc/resolv.conf is where I permanently configure DNS."

A better answer is:

“/etc/resolv.conf exposes resolver configuration to applications, but on many modern systems it is generated or managed by another networking component, so manually editing it may not persist.”

That's a strong DevOps detail.

16. The interview answer I'd memorize

If the interviewer asks:

“How does DNS resolution work? What are /etc/hosts and /etc/resolv.conf?”

Say:

“DNS translates hostnames into IP addresses. When an application needs to connect to a hostname, the OS uses its name-resolution configuration. On Linux, NSS in /etc/nsswitch.conf commonly determines the lookup order. With a typical hosts: files dns configuration, /etc/hosts is checked first, and if there is no match, the resolver uses the DNS servers configured through /etc/resolv.conf. Those DNS servers are usually recursive resolvers, which can query authoritative DNS servers if the answer isn't cached.”

Then:

“/etc/hosts contains local static hostname-to-IP mappings, while /etc/resolv.conf contains DNS resolver configuration such as nameservers, search domains and resolver options. In containers and Kubernetes, these files are particularly useful when troubleshooting service discovery and DNS problems.”

⭐ Commands I'd memorize for the interview
# Local hostname mappings
cat /etc/hosts

# DNS resolver configuration
cat /etc/resolv.conf

# Lookup order
cat /etc/nsswitch.conf

# Test name resolution
getent hosts example.com

# DNS query
dig example.com

# Query a specific DNS server
dig @8.8.8.8 example.com

# Alternative
nslookup example.com
The mental model
Application
     │
     ▼
OS / NSS
     │
     ├── /etc/hosts
     │
     └── DNS resolver
             │
             ▼
       /etc/resolv.conf
             │
             ▼
      Recursive DNS server
             │
             ▼
     Root → TLD → Authoritative
             │
             ▼
          IP address

Interview golden line:

“/etc/hosts is local name-to-IP mapping; /etc/resolv.conf tells the system where/how to perform DNS resolution; /etc/nsswitch.conf commonly determines the lookup order.”