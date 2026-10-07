```

•What is NAT? What are subnets and CIDR notation?

These are core networking concepts for DevOps interviews. You should understand them practically, especially in AWS, Kubernetes, Docker, and Linux networking.

1. What is NAT?

NAT = Network Address Translation.

NAT allows one IP address to be translated into another IP address, commonly allowing private IP addresses to access the internet through a public IP.

Simple example

Imagine an AWS private subnet:

Private EC2
10.0.1.10
     |
     | Internet request
     ↓
NAT Gateway
10.0.1.5
     |
     ↓
Public IP
     |
     ↓
Internet

The EC2 instance has:

10.0.1.10

This is a private IP, so it cannot directly communicate with the public internet.

The NAT Gateway translates the private source address when traffic goes out.

Before NAT:

10.0.1.10 → Internet

After NAT:

Public NAT IP → Internet

The response comes back through the NAT device, which translates the traffic back to the private instance.

Why do we need NAT in DevOps?

A very common AWS architecture is:

                    Internet
                       |
                Internet Gateway
                       |
              ┌────────┴────────┐
              ↓                 ↓
        Public Subnet      Private Subnet
              |                 |
        Load Balancer       EC2/EKS
                                |
                           NAT Gateway
                                |
                             Internet

The application servers can remain in a private subnet while still being able to:

Download packages
Pull container images
Access external APIs
Get OS updates

without having public IP addresses.

Interview answer

“NAT, or Network Address Translation, translates IP addresses between networks. In AWS, a common use is allowing instances in private subnets to initiate outbound internet connections through a NAT Gateway without exposing those instances directly to the internet.”

2. What is a subnet?

A subnet is a smaller network created from a larger IP network.

Suppose you have:

10.0.0.0/16

You could divide it into smaller networks:

10.0.1.0/24
10.0.2.0/24
10.0.3.0/24
...

Each subnet is an independent IP range.

In AWS, you might have:

VPC: 10.0.0.0/16

       |
       +-- Public subnet:  10.0.1.0/24
       |
       +-- Public subnet:  10.0.2.0/24
       |
       +-- Private subnet: 10.0.10.0/24
       |
       +-- Private subnet: 10.0.11.0/24

You can place different resources in different subnets.

For example:

Public subnet
   ↓
Load Balancer

Private subnet
   ↓
Application servers
   ↓
Database
3. What is CIDR notation?

CIDR = Classless Inter-Domain Routing.

CIDR describes an IP network using:

IP address / prefix length

For example:

10.0.0.0/24

The /24 tells us how many bits belong to the network portion.

IPv4 has 32 bits.

So:

/24

means:

24 network bits
8 host bits

Therefore:

2^8 = 256

total addresses.

For a traditional IPv4 subnet:

10.0.0.0/24

the range is:

10.0.0.0 → 10.0.0.255


4. CIDR examples you should know
| CIDR  | Total IPv4 addresses | Traditional usable hosts |
| ----- | -------------------: | -----------------------: |
| `/16` |               65,536 |                   65,534 |
| `/24` |                  256 |                      254 |
| `/25` |                  128 |                      126 |
| `/26` |                   64 |                       62 |
| `/27` |                   32 |                       30 |
| `/28` |                   16 |                       14 |
| `/30` |                    4 |                        2 |

A useful formula for a traditional IPv4 subnet is:

Total addresses = 2^(32 - prefix)

For /26:

2^(32-26)
= 2^6
= 64 addresses
5. Why is this important for DevOps?

You'll encounter CIDR everywhere.

AWS

When creating a VPC:

10.0.0.0/16

Then create subnets:

10.0.1.0/24
10.0.2.0/24
10.0.10.0/24
Kubernetes

Network policies often use CIDR ranges:

ipBlock:
  cidr: 10.0.0.0/16
Linux firewall

You might allow an entire network:

iptables -A INPUT -s 10.0.1.0/24 -j ACCEPT

Meaning:

Allow traffic originating from the 10.0.1.0/24 network.

Security groups / network ACLs

You might see:

10.0.0.0/16
0.0.0.0/0

0.0.0.0/0 means:

All IPv4 addresses.

So allowing:

0.0.0.0/0 → TCP 22

means SSH is accessible from anywhere, which is generally something you'd avoid unless there's a specific reason.

6. NAT vs Subnet vs CIDR

This is an easy way to remember them:

CIDR
 ↓
Defines an IP range

Subnet
 ↓
A smaller network created from an IP range

NAT
 ↓
Translates addresses between networks

Example:

VPC
10.0.0.0/16        ← CIDR

       |
       +---- Public subnet
       |     10.0.1.0/24
       |
       +---- Private subnet
             10.0.10.0/24
                    |
                    ↓
               NAT Gateway
                    |
                    ↓
                 Internet
⭐ Best interview answer

If the interviewer asks "What is NAT, subnet and CIDR?", give this:

“NAT stands for Network Address Translation and is used to translate IP addresses, commonly allowing private resources to access the internet through a public IP without exposing those resources directly. A subnet is a logical subdivision of a larger IP network. CIDR is the notation used to define an IP network range, such as 10.0.0.0/16 or 10.0.1.0/24. The number after the slash represents the network prefix length. For example, a /24 IPv4 network has 24 network bits and 8 host bits, giving 256 total addresses. In DevOps, I use these concepts when designing AWS VPCs, configuring Kubernetes networking, security groups, routing, and firewalls.”

🔥 Three things I'd memorize for interviews

NAT:

Private IP → NAT → Internet

Subnet:

Large network → smaller network

CIDR:

10.0.0.0/24
          ↑
     prefix length

If you understand these three diagrams, you're in good shape for the networking portion of a DevOps interview.