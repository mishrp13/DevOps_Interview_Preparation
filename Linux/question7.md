```
7.

Difference between /etc/passwd, /etc/shadow and /etc/group?

/etc/passwd vs /etc/shadow vs /etc/group — Interview Perspective

These three files are central to Linux user and group management.

A simple way to remember them:

/etc/passwd → User account information
/etc/shadow → Password & password-aging information
/etc/group  → Group information
1. /etc/passwd

/etc/passwd contains basic information about user accounts.

View it with:

cat /etc/passwd

A typical entry looks like:

john:x:1001:1001:John Doe:/home/john:/bin/bash

There are 7 fields, separated by :.

john
 ↓
x
 ↓
1001
 ↓
1001
 ↓
John Doe
 ↓
/home/john
 ↓
/bin/bash

| Field | Meaning                    |
| ----- | -------------------------- |
| 1     | Username                   |
| 2     | Password placeholder (`x`) |
| 3     | UID                        |
| 4     | Primary GID                |
| 5     | GECOS/comment/full name    |
| 6     | Home directory             |
| 7     | Login shell                |

Example
john:x:1001:1001:John Doe:/home/john:/bin/bash

means:

Username       → john
UID            → 1001
Primary GID    → 1001
Home           → /home/john
Shell          → /bin/bash
Important interview point

Modern Linux systems generally do not store the actual password hash in /etc/passwd.

The x means:

The password hash is stored in /etc/shadow.

2. /etc/shadow

/etc/shadow stores password hashes and password-aging information.

sudo cat /etc/shadow

A simplified entry looks like:

john:$6$....:20000:0:99999:7:::

The exact fields vary by system, but important ones include:

| Field | Meaning                   |
| ----- | ------------------------- |
| 1     | Username                  |
| 2     | Password hash             |
| 3     | Last password-change date |
| 4     | Minimum password age      |
| 5     | Maximum password age      |
| 6     | Warning period            |
| 7     | Inactivity period         |
| 8     | Account expiration        |
| 9     | Reserved                  |

Why is /etc/shadow protected?

Because it contains password hashes and sensitive password-aging information.

Typically:

ls -l /etc/passwd /etc/shadow

might show something conceptually like:

-rw-r--r--  /etc/passwd
-rw-r-----  /etc/shadow

So /etc/passwd is generally readable by ordinary users, while /etc/shadow is much more restricted.

Interview question

Q: Why can everyone read /etc/passwd but not /etc/shadow?

Answer:

/etc/passwd contains non-secret account information needed by many system utilities. /etc/shadow contains password hashes and sensitive password-aging information, so access is restricted.

3. /etc/group

/etc/group contains group definitions and group membership information.

cat /etc/group

Example:

developers:x:1002:alice,bob,john

There are generally four fields:

developers
     ↓
x
     ↓
1002
     ↓
alice,bob,john


| Field | Meaning                     |
| ----- | --------------------------- |
| 1     | Group name                  |
| 2     | Group password placeholder  |
| 3     | GID                         |
| 4     | Supplementary group members |

So:

developers:x:1002:alice,bob,john

means:

Group name → developers
GID        → 1002
Members    → alice, bob, john
4. How they work together

Suppose we have:

/etc/passwd

alice:x:1001:1002:Alice:/home/alice:/bin/bash

This tells us:

Alice
 UID = 1001
 Primary GID = 1002

Then:

/etc/group

developers:x:1002:alice,bob

The GID 1002 identifies the developers group.

So:

alice
 │
 ├── UID: 1001
 │
 └── Primary GID: 1002
                    │
                    └── developers
5. Primary group vs supplementary groups

This is another common interview question.

Primary group

The user's primary group is specified by the GID field in /etc/passwd.

Example:

alice:x:1001:1002:Alice:/home/alice:/bin/bash

Here:

UID  = 1001
GID  = 1002

GID 1002 is Alice's primary group.

Supplementary groups

Additional group memberships can be listed in /etc/group.

Example:

developers:x:1002:alice
docker:x:999:alice

Alice belongs to:

developers
docker

with developers potentially being her primary group depending on /etc/passwd.

You can check a user's groups with:

groups alice

or:

id alice
6. Very common interview question
Q: Where is the user's password stored?

Answer:

The password hash is stored in /etc/shadow, not /etc/passwd on a typical modern Linux system.

Q: Where is the user's UID stored?
/etc/passwd
Q: Where is the user's primary GID stored?
/etc/passwd
Q: Where are group definitions stored?
/etc/group
Q: Where are supplementary group memberships listed?
/etc/group
7. Don't confuse these three

Think of it this way:

┌──────────────────────────────┐
│        /etc/passwd           │
│                              │
│ User identity                │
│ UID                          │
│ Primary GID                  │
│ Home directory               │
│ Login shell                  │
└──────────────────────────────┘

┌──────────────────────────────┐
│        /etc/shadow           │
│                              │
│ Password hash                │
│ Password aging               │
│ Account expiration           │
└──────────────────────────────┘

┌──────────────────────────────┐
│         /etc/group           │
│                              │
│ Group name                   │
│ GID                          │
│ Group members                │
└──────────────────────────────┘
🧠 Interview one-liner

/etc/passwd stores user account and identity information, /etc/shadow stores password hashes and password-aging information, and /etc/group stores group definitions and supplementary group membership.

⭐ Bonus: commands interviewers may ask
id alice
# UID, GID and groups

getent passwd alice
# User information

getent group developers
# Group information

passwd alice
# Change/manage password

usermod -aG developers alice
# Add user to supplementary group

groups alice
# Show user's groups

One subtle but important point: these files are the traditional local account databases. On systems using LDAP, Active Directory integration, SSSD, or other NSS sources, commands such as getent can show accounts that aren't actually present in these local files
