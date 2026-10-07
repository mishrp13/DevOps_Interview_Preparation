```
•iptables basics: how do you open or block a port?

For a DevOps interview, you should know iptables at a practical level: what it does, how rules work, and how to allow/block traffic on a port.

⭐ Interview-ready answer

“iptables is a Linux firewall utility used to control network traffic. It works by inspecting packets and applying rules based on things like source IP, destination IP, protocol, and port. To open a port, I add an ACCEPT rule for that port. To block it, I add a DROP or REJECT rule. I also make sure the rule is placed correctly in the chain and saved so it persists after a reboot.”

1. What is iptables?

Think of it as a firewall inside Linux.

For example, suppose your application listens on:

8080

You can use iptables to control who can connect to it.

Internet
    |
    | TCP :8080
    ↓
Linux Server
    |
    ↓
iptables
    |
    ├── ACCEPT → Application
    │
    └── DROP → Traffic rejected
2. Important concepts

You should know these terms:

Chain

The most commonly discussed chains are:

INPUT
OUTPUT
FORWARD

For a server receiving traffic from the network, you usually care about:

INPUT

Think:

Incoming traffic → INPUT
Outgoing traffic → OUTPUT
Forwarded traffic → FORWARD
3. How do you open a port?

Suppose you want to allow TCP port 8080.

sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

Break it down:

-A INPUT

Add the rule to the INPUT chain.

-p tcp

Protocol is TCP.

--dport 8080

Destination port is 8080.

-j ACCEPT

Allow the traffic.

So:

Incoming TCP traffic
       ↓
Destination port 8080?
       ↓
      YES
       ↓
    ACCEPT
4. How do you block a port?

Suppose you want to block TCP port 8080:

sudo iptables -A INPUT -p tcp --dport 8080 -j DROP

DROP means the packet is silently discarded.

You can also use:

sudo iptables -A INPUT -p tcp --dport 8080 -j REJECT
DROP vs REJECT

This is a common interview question.

DROP:

Packet → silently discarded

The client generally gets no response.

REJECT:

Packet → rejected
       → client gets an error/rejection

Simple interview answer:

“DROP silently discards traffic, while REJECT actively tells the client that the traffic was rejected.”

5. Check existing rules

Very important command:

sudo iptables -L -n -v

Or:

sudo iptables -L INPUT -n -v

You might see:

Chain INPUT
target   prot  source      destination
ACCEPT   tcp   0.0.0.0/0   0.0.0.0/0   tcp dpt:22
ACCEPT   tcp   0.0.0.0/0   0.0.0.0/0   tcp dpt:8080
DROP     tcp   0.0.0.0/0   0.0.0.0/0   tcp dpt:3306

Meaning:

22    → allowed
8080  → allowed
3306  → blocked
6. Allow SSH — very important!

Before changing firewall rules remotely, be careful with SSH.

If SSH is running on:

22

you should make sure it's allowed:

sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

Otherwise, you could lock yourself out of the server.

This is an excellent practical point to mention in an interview.

7. Allow traffic only from a specific IP

Suppose only:

10.10.10.50

should access port 8080.

Use:

sudo iptables -A INPUT \
  -p tcp \
  -s 10.10.10.50 \
  --dport 8080 \
  -j ACCEPT

Now:

10.10.10.50 → 8080 → ACCEPT
Other IPs   → 8080 → depends on other rules

This is useful for restricting admin applications or internal services.

8. Delete a rule

First:

sudo iptables -L --line-numbers

Example:

num  target   prot  source      destination
1    ACCEPT   tcp   0.0.0.0/0   0.0.0.0/0   tcp dpt:22
2    ACCEPT   tcp   0.0.0.0/0   0.0.0.0/0   tcp dpt:8080
3    DROP     tcp   0.0.0.0/0   0.0.0.0/0   tcp dpt:3306

Delete rule number 3:

sudo iptables -D INPUT 3
9. Very important: rule order

iptables processes rules in order.

For example:

1. DROP TCP 8080
2. ACCEPT TCP 8080

The first rule matches, so the second rule won't help.

Therefore, rule ordering matters.

You can explain:

“iptables evaluates rules sequentially, so a broad DROP rule placed before a specific ACCEPT rule can prevent the ACCEPT rule from ever being reached.”

10. Default policy

You may see:

sudo iptables -L

and find:

Chain INPUT (policy ACCEPT)

This means incoming traffic is allowed by default unless a rule blocks it.

You could change it to:

sudo iptables -P INPUT DROP

But be extremely careful with this on a remote server.

You must first allow required traffic such as SSH, otherwise you may lose access.

11. Persistence

A common interview follow-up:

"Will iptables rules survive a reboot?"

Don't simply say yes.

Depending on the Linux distribution and configuration, rules may not automatically persist.

On Debian/Ubuntu, one common approach is:

sudo apt install iptables-persistent

and save the rules using:

sudo netfilter-persistent save

Modern Linux systems may also use nftables, and some environments use higher-level firewall tools such as firewalld or ufw.

So in an interview:

“iptables rules are runtime rules unless configured for persistence. The persistence mechanism depends on the Linux distribution; for example, Ubuntu/Debian can use iptables-persistent.”

🔥 A practical interview scenario

Interviewer:

"Our application runs on port 8080, but users can't access it. What would you check?"

A strong DevOps answer:

“First I'd verify that the application is actually listening on port 8080 using ss -lntp or a similar command. Then I'd check the local firewall using iptables -L -n -v and verify that TCP 8080 isn't being blocked. I'd also check cloud-level firewall rules such as AWS Security Groups or network ACLs if it's running in AWS. Finally, I'd test connectivity using curl or nc.”

For example:

ss -lntp | grep 8080

Then:

sudo iptables -L -n -v

And from another machine:

nc -vz SERVER_IP 8080

This is a much better DevOps answer than just knowing the iptables syntax because you're showing your troubleshooting approach.

⭐ Commands worth memorizing
# View rules
sudo iptables -L -n -v

# Allow port 8080
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

# Block port 8080
sudo iptables -A INPUT -p tcp --dport 8080 -j DROP

# Block with REJECT
sudo iptables -A INPUT -p tcp --dport 8080 -j REJECT

# Allow from a specific IP
sudo iptables -A INPUT -p tcp -s 10.10.10.50 --dport 8080 -j ACCEPT

# Show rule numbers
sudo iptables -L --line-numbers

# Delete rule
sudo iptables -D INPUT <rule-number>
🧠 Remember this pattern
iptables
   ↓
Chain
   ↓
Protocol (-p tcp)
   ↓
Port (--dport 8080)
   ↓
Action (-j ACCEPT/DROP/REJECT)

So if the interviewer says "Open TCP port 8080", your immediate answer should be:

sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

And then add: “I'd verify the rule and also check any upstream firewall/security group.”