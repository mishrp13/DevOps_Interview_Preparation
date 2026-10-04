```
Explain Partition , swap, boot process , file permissions ,Lvm 
Zombie process 
Basic commands like awk , sed , top etc 
Lvm 
Zombie process 
Basic commands like awk , sed , top etc 
Hard link and soft link 


Absolutely. These are very common Linux/DevOps interview topics. I’ll explain them in an interview-oriented way: what it is → why it matters → commands → practical DevOps example → interview answer.

1. Partition

A partition is a logical division of a physical disk.

Imagine a disk:

/dev/sda
┌─────────────────────────────────────┐
│             Physical Disk           │
├──────────────┬───────────┬──────────┤
│ /dev/sda1    │ /dev/sda2 │ /dev/sda3│
│    /         │   /home   │   swap   │
└──────────────┴───────────┴──────────┘

Each partition can have a different purpose.

For example:

/dev/sda1  → /
/dev/sda2  → /home
/dev/sda3  → swap
Common commands

See disks and partitions:

lsblk

More detailed disk information:

fdisk -l

Disk space:

df -h

Filesystem information:

lsblk -f
DevOps example

You have a server and want to check why an application is failing:

df -h

Output:

Filesystem      Size  Used Avail Use%
/dev/sda1        50G   48G    2G  96%

You immediately know the root filesystem is almost full.

Interview answer

"A partition is a logical division of a physical disk. We can create separate partitions for root, home, swap, or application data. In DevOps, I commonly use lsblk, fdisk -l, and df -h to inspect disk and filesystem usage."

2. Swap

Swap is disk space used as virtual memory when RAM is under pressure.

Suppose:

RAM = 8 GB
Swap = 4 GB

If RAM becomes heavily utilized, Linux can move some less-active memory pages to swap.

              Memory
                 │
        ┌────────▼────────┐
        │      RAM        │
        │      8 GB       │
        └────────┬────────┘
                 │
          RAM pressure
                 │
        ┌────────▼────────┐
        │      Swap       │
        │      4 GB       │
        │     Disk        │
        └─────────────────┘
Important

Swap is much slower than RAM because it uses disk.

So swap is not a replacement for sufficient RAM.

Check swap
free -h

or:

swapon --show

Example:

              total   used   free
Mem:           16Gi    14Gi    2Gi
Swap:           4Gi     1Gi    3Gi
Why DevOps cares

If a server starts heavily using swap, applications may become slow.

You can investigate with:

free -h
top
vmstat
Interview answer

"Swap is disk space that Linux can use as virtual memory when RAM is under pressure. It's slower than RAM, so heavy swap usage can indicate memory pressure and performance problems. I check it using free -h and swapon --show."

3. Linux Boot Process

This is a very common DevOps interview question.

The simplified boot process is:

Power ON
   ↓
BIOS / UEFI
   ↓
Bootloader
   ↓
Linux Kernel
   ↓
initramfs
   ↓
systemd
   ↓
Services
   ↓
Login

Let's understand each step.

Step 1: BIOS / UEFI

When the machine starts:

Power ON
   ↓
BIOS / UEFI

BIOS/UEFI performs hardware initialization and determines where to boot from.

For example:

Disk
USB
Network
Step 2: Bootloader

The bootloader loads the Linux kernel.

On many Linux systems, the bootloader is GRUB.

BIOS/UEFI
    ↓
GRUB
    ↓
Linux Kernel

GRUB can also provide multiple kernel choices.

Step 3: Kernel

The Linux kernel is loaded into memory.

The kernel:

initializes hardware
initializes memory management
initializes CPU
loads required drivers
starts the first userspace process
Step 4: initramfs

initramfs provides temporary userspace needed during early boot.

For example, it can contain drivers and tools needed to access the root filesystem.

Step 5: systemd

Modern Linux distributions commonly use:

systemd

as PID 1.

You can check:

ps -p 1

You might see:

PID 1 systemd

systemd starts services.

For example:

systemd
   ├── sshd
   ├── docker
   ├── nginx
   └── cron
Useful commands

Check boot time:

systemd-analyze

Check services:

systemctl status nginx

Check boot logs:

journalctl -b
Interview answer

"The Linux boot process generally starts with BIOS or UEFI, which initializes hardware and loads the bootloader such as GRUB. GRUB loads the Linux kernel and initramfs. The kernel initializes the system and starts PID 1, usually systemd, which then starts the required services and brings the system to the appropriate target."

4. File Permissions

Linux permissions are extremely important for DevOps.

Run:

ls -l

Example:

-rwxr-xr-- 1 devops devops 1200 Oct 4 deploy.sh

Break it down:

- rwx r-x r--
│ │   │   │
│ │   │   └── Others
│ │   └────── Group
│ └────────── Owner
└──────────── File type

There are three permission categories:

u = user/owner
g = group
o = others

And three basic permissions:

r = read
w = write
x = execute
Numeric permissions
r = 4
w = 2
x = 1

Therefore:

rwx = 7
rw- = 6
r-x = 5
r-- = 4

Example:

chmod 755 deploy.sh

means:

Owner  → rwx = 7
Group  → r-x = 5
Others → r-x = 5

So:

755 = rwxr-xr-x

Another common example:

chmod 644 config.txt

means:

Owner  → rw-
Group  → r--
Others → r--
Important commands

Change permissions:

chmod 755 script.sh

Change owner:

chown devops:devops script.sh

Change group:

chgrp developers script.sh

Check permissions:

ls -l
DevOps example

You deploy:

./deploy.sh

and get:

Permission denied

Check:

ls -l deploy.sh

Maybe:

-rw-r--r-- deploy.sh

The file doesn't have execute permission.

You can fix it:

chmod +x deploy.sh
Interview answer

"Linux permissions control who can read, write, or execute a file. Permissions are defined for owner, group, and others. I use chmod to modify permissions and chown to modify ownership. For example, chmod 755 script.sh gives the owner read/write/execute and the group and others read/execute permissions."

5. LVM — Logical Volume Manager

LVM is very important for Linux/DevOps interviews.

LVM allows you to manage storage more flexibly than traditional fixed partitions.

The basic structure is:

Physical Disk / Partition
          ↓
   Physical Volume (PV)
          ↓
   Volume Group (VG)
          ↓
   Logical Volume (LV)
          ↓
      Filesystem
          ↓
       Mount Point

Think:

Disk
 ↓
PV
 ↓
VG
 ↓
LV
 ↓
Filesystem
 ↓
/data
Physical Volume — PV

A disk or partition initialized for LVM.

Example:

pvcreate /dev/sdb

Check:

pvs
Volume Group — VG

A pool of storage made from one or more physical volumes.

vgcreate datavg /dev/sdb

Check:

vgs
Logical Volume — LV

A logical disk created from the volume group.

lvcreate -L 10G -n applv datavg

Check:

lvs

Then create a filesystem:

mkfs.ext4 /dev/datavg/applv

Create mount point:

mkdir /app

Mount:

mount /dev/datavg/applv /app
Why LVM is useful

Suppose:

/app = 100 GB

and it becomes full.

With LVM, you can often extend the logical volume:

lvextend -L +20G /dev/datavg/applv

Then grow the filesystem as appropriate.

For ext4, for example:

resize2fs /dev/datavg/applv

For XFS:

xfs_growfs /app

The exact procedure depends on filesystem type.

Interview answer

"LVM provides flexible storage management. The hierarchy is PV, VG, and LV. Physical volumes are combined into volume groups, and logical volumes are created from those groups. One major advantage is that logical volumes can be extended more flexibly as storage requirements grow."

6. Zombie Process

This is another classic interview question.

A zombie process is a process that has finished execution but still has an entry in the process table because its parent hasn't collected its exit status.

Think:

Parent
  │
  └── Child
       │
       └── finishes
              ↓
          ZOMBIE

The child is already dead.

But its process table entry remains until the parent calls wait()/waitpid() and collects the exit status.

How to identify zombies

Run:

ps aux

You may see:

user  1234  ...  Z  ...  [process] <defunct>

Z means zombie.

Another useful command:

ps -eo pid,ppid,state,cmd

Look for:

Z
Why zombies happen

Typical sequence:

Parent creates child
       ↓
Child finishes
       ↓
Child becomes zombie
       ↓
Parent should call wait()
       ↓
Zombie entry removed

If the parent doesn't properly reap the child, zombies can accumulate.

Can you kill a zombie?

This is a common interview trick.

No, not directly.

The process has already terminated.

You need to address the parent process so it reaps the child.

Find the parent:

ps -o pid,ppid,state,cmd -p <PID>

Then investigate the parent process.

DevOps example

A badly written application repeatedly creates child processes and doesn't reap them.

Eventually you may see many:

<defunct>

processes.

That can indicate an application/process-management problem.

Interview answer

"A zombie is a child process that has finished execution but whose parent hasn't collected its exit status using wait() or waitpid(). It remains as a process-table entry. I can identify zombies using ps and look for state Z or <defunct>. A zombie itself can't really be killed because it's already terminated; the parent needs to reap it."

7. top

top is one of the most useful Linux troubleshooting commands.

Run:

top

It provides real-time information about:

CPU
memory
load
processes
process IDs
CPU usage
memory usage

Example:

PID    USER    %CPU   %MEM    COMMAND
1234   root    95.2   10.1    java
5678   app     20.3    5.2    python

If CPU is high:

%CPU = 95%

you can investigate that process.

Useful related commands
htop

if installed.

Specific process:

top -p 1234
DevOps troubleshooting example

Application is slow.

You might start with:

top

Then:

free -h
df -h
ps aux

This helps determine whether the problem is CPU, memory, disk, or a particular process.

8. ps

ps shows currently running processes.

ps aux

Useful for:

Who is running?
What process?
What PID?
How much CPU?
How much memory?

Find a process:

ps aux | grep nginx

Better:

pgrep -a nginx
9. grep

grep searches text.

Example:

grep "ERROR" application.log

Find errors in a log.

Case-insensitive:

grep -i "error" application.log

Count matches:

grep -c "ERROR" application.log

Search recursively:

grep -r "ERROR" /var/log/
DevOps example
grep "500" access.log

Find HTTP 500 responses.

10. awk

awk is extremely useful for structured text processing.

Suppose:

192.168.1.10 GET /home 200
10.0.0.5 GET /login 500
192.168.1.10 GET /api 200

You want the IP addresses.

awk '{print $1}' access.log

Output:

192.168.1.10
10.0.0.5
192.168.1.10

Because:

$1 = first column
$2 = second column
$3 = third column

For example:

awk '{print $1, $4}' access.log

prints column 1 and 4.

Count HTTP 500 errors

If status code is column 4:

awk '$4 == 500 {count++} END {print count}' access.log

This means:

$4 == 500
     ↓
if column 4 is 500

count++
     ↓
increase counter

END
 ↓
print count
Interview answer

"awk is useful for field-based text processing. I commonly use it to extract columns from logs, filter records, and perform simple calculations."

11. sed

sed is mainly used for stream editing.

For example:

sed 's/old/new/g' file.txt

Replace:

old

with:

new

g means replace all occurrences on each line.

Example

File:

server=dev
environment=dev

Run:

sed 's/dev/prod/g' config.txt

Output:

server=prod
environment=prod
Delete lines

Delete line 2:

sed '2d' file.txt

Delete lines containing DEBUG:

sed '/DEBUG/d' application.log
DevOps use case

In deployment automation, you may need to update a configuration file:

sed -i 's/ENVIRONMENT=dev/ENVIRONMENT=prod/' config.env

-i modifies the file in place.

Interview answer

"sed is a stream editor commonly used for searching, replacing, deleting, or transforming text. In DevOps I commonly use it for automated configuration changes and log manipulation."

12. tail

Shows the end of a file.

tail application.log

By default, it shows the last 10 lines.

For live logs:

tail -f application.log

This is extremely useful during deployments.

Example:

tail -f /var/log/nginx/access.log

You can watch new log entries appear in real time.

13. head

Shows the beginning of a file:

head application.log

First 20 lines:

head -n 20 application.log
14. df

Shows filesystem disk usage.

df -h

Example:

Filesystem      Size  Used Avail Use%
/dev/sda1        50G   48G    2G  96%
DevOps troubleshooting

If an application cannot write logs:

df -h

Maybe the filesystem is:

96%

or:

100%
15. du

Shows how much disk space files/directories consume.

du -sh /var/log

Find large directories:

du -sh /var/log/*

Typical troubleshooting:

df -h

says disk is full.

Then:

du -sh /var/log/*

helps identify what's consuming space.

16. free

Check memory:

free -h

Example:

               total   used   free
Mem:            16G     14G     2G
Swap:            4G      1G     3G

Useful when troubleshooting:

Out of memory
High memory usage
Swap usage
17. kill

Send a signal to a process.

kill 1234

By default this sends:

SIGTERM

which politely asks the process to terminate.

If it doesn't stop:

kill -9 1234

This sends:

SIGKILL

which cannot be caught or ignored by the process.

Interview tip

Don't immediately say:

"I use kill -9."

A better answer:

"I'd normally send SIGTERM first so the application can shut down gracefully. I'd use SIGKILL only if the process doesn't terminate and there's a reason to force it."

18. Hard Link vs Soft Link

This is another very common Linux interview question.

Hard Link

A hard link is another directory entry pointing to the same underlying inode/data.

           ┌──────────────┐
file1 ────►│              │
           │    inode     │
file2 ────►│     data     │
           └──────────────┘

Create:

ln original.txt hardlink.txt

Now:

original.txt
hardlink.txt

both refer to the same underlying file data.

Check inode:

ls -li

You will see the same inode number.

Soft Link / Symbolic Link

A symbolic link is a separate file that points to another pathname.

symlink
   │
   └──────────► original.txt

Create:

ln -s original.txt symlink.txt

Check:

ls -l

You'll see something like:

symlink.txt -> original.txt
Hard vs Soft Link
Feature	Hard Link	Soft Link
Points to	Same inode	Pathname
Different filesystem	Generally no	Yes
Directory	Generally not allowed	Yes
If original deleted	Data still accessible through hard link	Link becomes broken
ls -li inode	Same	Different
Can link directories	Generally no	Yes
Important interview example

Suppose:

echo "hello" > original.txt
ln original.txt hard.txt
ln -s original.txt soft.txt

Now:

original.txt
hard.txt
soft.txt → original.txt

Delete:

rm original.txt

What happens?

Hard link
cat hard.txt

still works:

hello

Because hard.txt points to the same inode/data.

Soft link
cat soft.txt

fails because:

soft.txt → original.txt

but original.txt no longer exists.

So the symbolic link is broken.

Why DevOps engineers care about links

A very common real-world example is:

/opt/app/releases/
    release-101/
    release-102/
    release-103/

        ↓

/opt/app/current -> /opt/app/releases/release-103

current can be a symbolic link.

During deployment:

current → release-103

After deploying a new version:

current → release-104

This gives you a simple release-switching mechanism.

You can also roll back:

current → release-103

This pattern is commonly associated with atomic-ish release switching, although the exact deployment safety depends on how the application and filesystem are managed.

🔥 DevOps Interview Cheat Sheet
Topic	Remember
Partition	Logical division of disk
Swap	Disk used as virtual memory
Boot	BIOS/UEFI → GRUB → Kernel → systemd → services
Permissions	r=4, w=2, x=1
chmod	Change permissions
chown	Change ownership
LVM	PV → VG → LV → filesystem
Zombie	Finished child not reaped by parent
top	Real-time process/resource monitoring
ps	Process information
grep	Search text
awk	Field/column processing
sed	Stream editing/replacement
tail -f	Follow live logs
head	First lines
df -h	Filesystem disk usage
du -sh	Directory/file disk usage
free -h	Memory/swap usage
kill	Send signal to process
Hard link	Same inode
Soft link	Points to pathname
⭐ 10 Questions You Should Be Ready For

For a DevOps interview, I would especially prepare these:

Explain the Linux boot process.
What is LVM? Explain PV, VG, and LV.
What is the difference between df and du?
What is a zombie process? Can you kill a zombie?
Explain Linux file permissions and chmod 755.
What is the difference between hard and soft links?
How would you troubleshoot a server with high CPU?
How would you troubleshoot a server with low disk space?
How would you use awk and sed in a deployment script?
How would you investigate an application that suddenly becomes slow?

For the last one, a strong DevOps troubleshooting flow is:

Application slow
      ↓
top / uptime
      ↓
CPU?
      ↓
free -h
      ↓
Memory?
      ↓
df -h
      ↓
Disk full?
      ↓
iostat / vmstat
      ↓
Disk / I/O?
      ↓
ps / logs
      ↓
Which process/application?
      ↓
grep / awk / tail
      ↓
Find root cause

That kind of structured troubleshooting approach is often more valuable in a DevOps interview than simply memorizing Linux commands.
