```

6. df -h vs du -sh: why can they show different numbers?

df -h vs du -sh — Interview Perspective

This is a very common Linux interview question.

The short answer is:

df looks at filesystem-level disk usage, while du looks at the disk space used by files/directories.

Because they measure different things, their numbers can differ.

1. What does df -h show?

df = disk free

df -h

It reports filesystem-level information:

Filesystem      Size  Used Avail Use%
/dev/sda1       100G   70G   30G  70%

It answers:

How much space is used/free on this filesystem?

-h means human-readable, so you get G, M, etc.

2. What does du -sh show?

du = disk usage

du -sh /var

It estimates the amount of disk space consumed by the files under /var.

Options:

-s → summary
-h → human-readable

For example:

du -sh /var

might show:

45G    /var

It answers:

How much space is being consumed by files under this directory?

3. Why can they show different numbers?

Suppose:

df -h /

shows:

Filesystem      Size  Used Avail Use%
/dev/sda1       100G   70G   30G  70%

But:

du -sh /

shows:

55G    /

You might ask:

"Where did the other 15 GB go?"

There are several common reasons.

Reason 1: Deleted files still held open by processes ⭐

This is one of the most important interview answers.

Suppose a process opens:

/var/log/app.log

and the file is 10 GB.

Then someone deletes it:

rm /var/log/app.log

The filename disappears.

So:

du

cannot see it anymore.

But if the process still has the file open, the filesystem blocks remain allocated.

Therefore:

df → still counts the 10 GB
du → doesn't count it

You can find these files with:

sudo lsof +L1

or:

sudo lsof | grep deleted
Interview answer

A deleted file can continue consuming disk space if a running process still has it open. du doesn't see the deleted pathname, but df still sees the allocated filesystem blocks.

This is a classic production troubleshooting scenario.

4. Reason 2: Different filesystems / mount points

Consider:

/
├── home/
├── var/
└── data/

Suppose /data is actually a separate filesystem.

df -h

might show:

/dev/sda1   100G   60G
/dev/sdb1   500G  200G

But when you run:

du -sh /

the result depends on how du traverses mounted filesystems and the options used.

By default, du can cross into mounted directories, which can make interpretation tricky.

To stay on the same filesystem:

du -xsh /

-x means:

Stay on one filesystem.

This is very useful when troubleshooting disk usage.

5. Reason 3: Filesystem overhead

df accounts for filesystem-level space usage, including things that aren't ordinary user-visible files.

For example, filesystems maintain:

Metadata
Journaling information
Allocation structures
Reserved blocks

du primarily accounts for the disk usage of files/directories it can traverse.

Therefore:

df ≠ sum of du

This difference can be normal.

6. Reason 4: Sparse files

A sparse file can have a very large apparent size while using relatively little actual disk space.

For example:

truncate -s 10G sparse.img

The file may report a size of 10 GB, but it doesn't necessarily consume 10 GB of actual blocks.

You can compare:

ls -lh sparse.img
du -h sparse.img

You may see something like:

ls  → 10G
du  → 0

This happens because:

ls → apparent/logical size
du → allocated disk blocks
7. A useful mental model

Think of:

df

Looking at the warehouse:

Filesystem
┌──────────────────────────┐
│ Used blocks              │
│ Metadata                 │
│ Journal                  │
│ Reserved space           │
│ Free blocks              │
└──────────────────────────┘

It asks:

"How full is the entire filesystem?"

du

Looking at the items stored in the warehouse:

Directory
├── file1
├── file2
├── logs
└── database

It asks:

"How much space do these visible files/directories consume?"

⭐ Classic interview scenario

Interviewer:

df -h says / is 90% full, but du -sh /* doesn't add up to the same amount. What would you check?

A strong answer:

First, I'd check for deleted-but-open files using lsof +L1. Then I'd check whether there are separate mounted filesystems, use du -x to stay within the filesystem, and consider filesystem metadata/reserved space. I'd also check for sparse files if apparent and allocated sizes seem inconsistent.

Useful commands:

df -h
du -xsh /
sudo lsof +L1
findmnt
lsblk -f
df vs du — Quick Interview Table

|                          | `df -h`                           | `du -sh`                                  |
| ------------------------ | --------------------------------- | ----------------------------------------- |
| Measures                 | Filesystem usage                  | File/directory usage                      |
| Scope                    | Entire filesystem                 | Selected directory/files                  |
| Shows free space?        | ✅ Yes                             | ❌ No                                      |
| Sees deleted-open files? | ✅ Yes                             | ❌ No                                      |
| Filesystem metadata?     | Included in filesystem accounting | Not normally represented as regular files |
| Common use               | "Why is disk full?"               | "Which directory is using space?"         |
| `-h`                     | Human-readable                    | Human-readable                            |
| `-s`                     | —                                 | Summary                                   |
| `-x`                     | —                                 | Stay on one filesystem                    |

🧠 One-line interview answer

df reports filesystem-level block usage, while du calculates usage from files/directories it can see. They can differ because of deleted-but-open files, mounted filesystems, filesystem metadata/reserved space, and sparse files.
