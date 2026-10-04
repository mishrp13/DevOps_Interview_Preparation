```

5. What does /etc/fstab do? What does mounting mean?

Mounting means making a filesystem available at a particular directory (mount point) in the Linux directory tree.

For example, suppose you have a disk partition:

/dev/sdb1

You can mount it at:

/data
sudo mount /dev/sdb1 /data

Now the filesystem stored on /dev/sdb1 becomes accessible through:

/data

Conceptually:

/dev/sdb1
   │
   │ mount
   ▼
 /data
   │
   ├── file1.txt
   ├── file2.txt
   └── logs/
Interview definition

Mounting is the process of attaching a filesystem to a directory in the Linux filesystem hierarchy so that its contents become accessible through that directory.

2. What is a mount point?

A mount point is the directory where a filesystem is attached.

Example:

mount /dev/sdb1 /data

Here:

/dev/sdb1 → device/filesystem
/data      → mount point

Common mount points include:

/
/home
/var
/mnt
/media
/data
3. What is /etc/fstab?

/etc/fstab stands for filesystem table.

It is a configuration file that tells Linux:

Which filesystems should be mounted, where they should be mounted, and with what options.

Typical location:

/etc/fstab

Example:

UUID=abc123  /data  ext4  defaults  0  2

This tells Linux:

UUID=abc123
      ↓
mount this filesystem
      ↓
at /data
      ↓
filesystem type = ext4
      ↓
use defaults
4. Why is /etc/fstab important?

One of its main purposes is persistent mounting.

Suppose you manually run:

mount /dev/sdb1 /data

It works now.

But after reboot, the system may not automatically mount it.

If you put the filesystem in /etc/fstab, Linux can mount it automatically during boot.

Boot
 ↓
Read /etc/fstab
 ↓
Identify configured filesystems
 ↓
Mount them
 ↓
Filesystem available
Interview answer

/etc/fstab contains persistent filesystem mount configuration. It specifies what filesystem to mount, the mount point, filesystem type, mount options, and filesystem-check settings.

5. Understanding an /etc/fstab entry

A typical entry:

UUID=1234-ABCD  /data  ext4  defaults  0  2

There are 6 fields:

| Field | Meaning               | Example          |
| ----- | --------------------- | ---------------- |
| 1     | Device/filesystem     | `UUID=1234-ABCD` |
| 2     | Mount point           | `/data`          |
| 3     | Filesystem type       | `ext4`           |
| 4     | Mount options         | `defaults`       |
| 5     | `dump` backup setting | `0`              |
| 6     | `fsck` check order    | `2`              |

The first four are particularly important in interviews.
6. Why use UUID instead of /dev/sdb1?

You might see:

/dev/sdb1 /data ext4 defaults 0 2

But preferably:

UUID=xxxx /data ext4 defaults 0 2

Why?

Device names such as:

/dev/sda
/dev/sdb

can potentially change depending on how devices are detected.

A filesystem's UUID is intended to uniquely identify that filesystem.

You can find UUIDs with:

blkid

or:

lsblk -f
7. What does mount -a do?

Very common interview question.

sudo mount -a

means:

Mount all filesystems configured in /etc/fstab that are not already mounted, subject to their options.

This is very useful after editing /etc/fstab.

For example:

sudo vi /etc/fstab
sudo mount -a

You can test whether your entry works without rebooting.

8. What happens if /etc/fstab is wrong?

This is an important real-world point.

Suppose you add:

UUID=wrong-value /data ext4 defaults 0 2

The filesystem cannot be found.

Depending on the configuration and system, this can cause boot problems or leave the system waiting for/failing to mount the filesystem.

So after modifying /etc/fstab, test it:

sudo mount -a

Then check:

mount

or:

findmnt
9. Mount vs unmount

Mount:

sudo mount /dev/sdb1 /data

Unmount:

sudo umount /data

Notice the command is:

umount

not unmount.

Why might umount fail?

If the filesystem is busy—for example, a process has a file open or a shell's current directory is inside the mounted filesystem.

You might see:

target is busy

Useful commands:

lsof /data

or:

fuser -m /data
⭐ Common interview questions
Q1. What is mounting?

Mounting attaches a filesystem to a directory, called the mount point, making its contents accessible through that directory.

Q2. What is /etc/fstab?

/etc/fstab is the filesystem table containing persistent filesystem mount configurations used during boot and by mount utilities.

Q3. What are the fields in /etc/fstab?
filesystem
mount point
filesystem type
mount options
dump
fsck order
Q4. Difference between mount and /etc/fstab?
mount command
     ↓
Usually performs a mount operation now

/etc/fstab
     ↓
Stores mount configuration
     ↓
Can be used for automatic/persistent mounting
Q5. Why use UUID?

UUID provides a stable identifier for a filesystem instead of relying on a potentially changing device name such as /dev/sdb1.

Q6. How do you test /etc/fstab without rebooting?
sudo mount -a
🧠 Easy way to remember

Think of a filesystem as a storage room and the mount point as its door:

Disk / filesystem
       │
       │ mount
       ▼
     /data
       │
       └── accessible files

/etc/fstab is the instruction sheet telling Linux:

"At boot, attach this storage room to this door using these settings."

One-line interview answer:

Mounting makes a filesystem accessible at a directory, while /etc/fstab stores the configuration for filesystems that should be mounted, typically persistently across reboots.
