```
•How does SSH work? Key-based auth, ssh-agent, config file, tunnelling?

Absolutely — for a DevOps interview, you should understand SSH not just as “a command to connect to a server,” but also how authentication, keys, agents, configuration, and tunneling work.

🔐 SSH — Secure Shell

SSH (Secure Shell) is a secure protocol used to remotely access Linux/Unix systems over an encrypted connection.

Default port:

TCP 22

Typical DevOps usage:

ssh user@server-ip

For example:

ssh ubuntu@10.0.1.25

It is commonly used for:

Connecting to EC2/Linux servers
Running remote commands
Copying files using scp/sftp
Git authentication
Ansible
Port forwarding/tunneling
Troubleshooting production servers
1. How does SSH work?

Suppose your laptop connects to an EC2 server:

Your Laptop
    |
    | SSH TCP/22
    |
    v
+------------------+
| EC2 / Linux      |
| SSH Server       |
| sshd             |
+------------------+

When you run:

ssh ubuntu@10.0.1.25

roughly this happens:

Step 1 — TCP connection

Your client connects to port 22:

Client → Server: TCP 22
Step 2 — SSH protocol negotiation

Client and server negotiate:

SSH protocol version
Encryption algorithms
Key-exchange algorithms
MAC/integrity algorithms
Step 3 — Key exchange

The client and server establish shared cryptographic session keys.

These keys are used to encrypt the communication.

Client                         Server
  |                              |
  |---- key exchange ---------->|
  |<--- key exchange ------------|
  |                              |
  |==== encrypted session =======|
Step 4 — Server authentication

Your client verifies the server's identity using its host key.

This helps protect against man-in-the-middle attacks.

You'll often see:

The authenticity of host 'server' can't be established.
Are you sure you want to continue connecting (yes/no)?

After accepting, the server's host key is stored in:

~/.ssh/known_hosts
Step 5 — User authentication

Now the server needs to verify you.

Common methods:

Password authentication
Key-based authentication

For DevOps, key-based authentication is preferred.

2. SSH Key-Based Authentication ⭐

Instead of using a password, SSH uses a key pair.

You have:

Private key              Public key
-----------              ----------
id_ed25519               id_ed25519.pub
id_rsa                   id_rsa.pub

The important rule:

Private key stays with you. Public key goes to the server.

Example:

Your Laptop
+-----------------------+
| private key           |
| ~/.ssh/id_ed25519     |
+-----------------------+
           |
           | public key installed
           v
+-----------------------+
| EC2 Server            |
| ~/.ssh/authorized_keys|
+-----------------------+

Generate a key:

ssh-keygen -t ed25519

You'll typically get:

~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub

View the public key:

cat ~/.ssh/id_ed25519.pub

The server stores your public key in:

~/.ssh/authorized_keys

Then:

ssh ubuntu@10.0.1.25

SSH uses the private key to prove that you possess the corresponding private key.

Important interview point

The private key is not sent over the network.

That's a very important concept.

3. authorized_keys

On the server:

~/.ssh/authorized_keys

contains authorized public keys.

Example:

ssh-ed25519 AAAAC3... user@laptop
ssh-ed25519 AAAAXYZ... devops@company

If your public key is present there and permissions/configuration are correct, SSH can authenticate you.

Typical permissions:

chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

Private key on your machine should also be protected:

chmod 600 ~/.ssh/id_ed25519
4. What is ssh-agent?

This is a very common DevOps interview question.

Imagine you have:

10 servers

and your private key is protected with a passphrase.

You don't want to type that passphrase every time you SSH.

That's where ssh-agent comes in.

             ssh-agent
                 |
       +---------+---------+
       |                   |
    SSH key             SSH key
       |                   |
 Server A              Server B

Start the agent:

eval "$(ssh-agent -s)"

Add your private key:

ssh-add ~/.ssh/id_ed25519

Check loaded keys:

ssh-add -l

Now when you SSH:

ssh user@server1
ssh user@server2
ssh user@server3

the agent can perform the authentication using the loaded key.

Why is this useful in DevOps?

Especially with:

Git
Ansible
Bastion hosts
Multiple servers
CI/CD workflows
SSH-based automation
Interview answer

“ssh-agent securely keeps private keys available in memory so I don't have to repeatedly enter the key passphrase when connecting to multiple servers.”

5. SSH Config File ⭐

Instead of repeatedly typing:

ssh -i ~/.ssh/id_ed25519 ubuntu@10.0.1.25

you can configure:

~/.ssh/config

Example:

Host web-server
    HostName 10.0.1.25
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519

Now simply:

ssh web-server

SSH automatically uses:

HostName      → 10.0.1.25
User          → ubuntu
IdentityFile  → ~/.ssh/id_ed25519
6. SSH Config with Bastion Host

This is especially useful in AWS.

Suppose your architecture is:

Internet
   |
   v
Bastion Host
Public subnet
   |
   | SSH
   v
Private EC2
10.0.2.15

The private server isn't directly reachable from the internet.

You can configure:

Host bastion
    HostName 203.0.113.10
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519

Host private-server
    HostName 10.0.2.15
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump bastion

Now:

ssh private-server

SSH automatically goes:

Laptop
   |
   | SSH
   v
Bastion
   |
   | SSH
   v
Private EC2

This is a very good DevOps interview example.

7. SSH Tunneling / Port Forwarding ⭐⭐⭐

SSH can also create an encrypted tunnel between machines.

There are three important concepts:

Local forwarding
Remote forwarding
Dynamic forwarding
A. Local Port Forwarding — -L

Suppose your database is private:

Laptop
   |
   X
Internet
   |
Private DB
10.0.2.20:5432

You cannot directly access:

10.0.2.20:5432

But you can SSH through a bastion.

ssh -L 5432:10.0.2.20:5432 ubuntu@bastion

Now:

localhost:5432
      |
      | SSH encrypted tunnel
      v
Bastion
      |
      v
10.0.2.20:5432

Your local machine can connect to:

localhost:5432

and SSH forwards that traffic to:

10.0.2.20:5432
Syntax
ssh -L <local-port>:<destination>:<destination-port> user@ssh-server

Example:

ssh -L 8080:10.0.2.15:8080 ubuntu@bastion

Then:

localhost:8080
      ↓
SSH tunnel
      ↓
bastion
      ↓
10.0.2.15:8080

This is commonly used to access:

Private databases
Internal web applications
Kubernetes dashboards
Internal monitoring systems
8. Remote Port Forwarding — -R

This is the opposite direction.

Example:

ssh -R 8080:localhost:3000 user@server

Conceptually:

Remote Server :8080
       |
       | SSH tunnel
       v
Your Machine :3000

Useful when you want a remote machine to access something running on your local machine.

9. Dynamic Port Forwarding — -D

SSH can also create a SOCKS proxy:

ssh -D 1080 user@server

Now your applications can use:

SOCKS5 localhost:1080

Traffic can be routed through the SSH server.

This is called:

Dynamic port forwarding

10. SSH Tunneling Summary
Type	Option	Direction
Local forwarding	-L	Local → Remote
Remote forwarding	-R	Remote → Local
Dynamic forwarding	-D	SOCKS proxy

For interviews, remember:

-L = Local
-R = Remote
-D = Dynamic
11. SSH Security in DevOps

As a DevOps engineer, you should mention security.

Disable password authentication

In /etc/ssh/sshd_config:

PasswordAuthentication no

Use SSH keys instead.

Don't allow root login
PermitRootLogin no

Then restart/reload SSH according to your distro:

sudo systemctl reload ssh

or:

sudo systemctl reload sshd
Restrict SSH access

At the network level:

Internet
   |
Security Group
   |
Port 22
   |
Bastion

Ideally, don't expose SSH to everyone:

0.0.0.0/0

Instead restrict it to:

Corporate VPN
Bastion
Trusted IP ranges
Zero-trust access mechanism
12. SSH Troubleshooting — Very Important for DevOps

If:

ssh user@server

doesn't work, troubleshoot layer by layer.

1. Can I reach port 22?
nc -vz server-ip 22

or:

telnet server-ip 22
2. Is SSH server running?

On server:

sudo systemctl status ssh

or:

sudo systemctl status sshd
3. Is port 22 listening?
sudo ss -lntp | grep :22
4. Check firewall
sudo iptables -L -n -v

or depending on distro:

sudo ufw status
5. Check AWS Security Group

Make sure inbound TCP 22 is allowed from the expected source.

6. Check key permissions
chmod 600 ~/.ssh/id_ed25519
7. Use verbose SSH

This is extremely useful:

ssh -v user@server

More verbose:

ssh -vvv user@server

It helps identify whether the problem is:

Network
   ↓
TCP
   ↓
SSH handshake
   ↓
Authentication
   ↓
Authorization
13. Important SSH Files
Client side
~/.ssh/
├── id_ed25519          # Private key
├── id_ed25519.pub      # Public key
├── known_hosts         # Server host keys
└── config              # SSH client configuration
Server side
/etc/ssh/sshd_config    # SSH server configuration

~/.ssh/authorized_keys  # Authorized user public keys

Remember:

Private key       → Client
Public key        → Server
known_hosts       → Client remembers server identity
authorized_keys   → Server knows allowed client keys
⭐ Best Interview Answer

If the interviewer asks:

“How does SSH work and what are key-based authentication, ssh-agent, config, and tunneling?”

You can answer:

“SSH is a secure protocol, normally running on TCP port 22, used for remote administration and secure communication. The client and server first establish an encrypted session through key exchange, and then the client authenticates to the server. In DevOps, I prefer key-based authentication where the private key stays on the client and the corresponding public key is stored in the user's authorized_keys on the server.

ssh-agent allows me to load a private key into an agent so I don't have to repeatedly enter its passphrase. The ~/.ssh/config file lets me define reusable connection settings such as hostname, user, identity file, and ProxyJump for bastion hosts.

SSH also supports tunneling. -L is local port forwarding, commonly used to access private databases or internal services through a bastion; -R is remote forwarding, and -D provides dynamic SOCKS proxying.

From a DevOps perspective, I also secure SSH by using key-based authentication, disabling unnecessary password/root login, restricting port 22 using security groups or firewalls, and troubleshooting with ssh -vvv, ss, firewall checks, and network connectivity tests.”

The mental model to remember
                 SSH
                  |
       +----------+----------+
       |          |          |
   Auth       Config      Tunneling
     |           |            |
 SSH Keys    ~/.ssh/config   -L / -R / -D
     |
 +---+---+
 |       |
Private  Public
 Key     Key
 |       |
Client   Server
         |
    authorized_keys

If you remember private key → public key → ssh-agent → config → bastion/ProxyJump → -L/-R/-D, you're in a strong position for most SSH questions in a DevOps interview.