```


4. What is umask?

umask (user file-creation mask) determines the default permissions that are removed when a new file or directory is created.

1. Basic idea

When Linux creates a new object, it starts with a maximum base permission:

Regular file     → 666  (rw-rw-rw-)
Directory        → 777  (rwxrwxrwx)

Then the umask removes permissions from that base.

For example:

umask 022
New file
666
-022
----
644

So a newly created file gets:

rw-r--r--
New directory
777
-022
----
755

So a newly created directory gets:

rwxr-xr-x
2. Why isn't a new file 755?

This is a common interview question.

Because regular files start from 666, not 777.

File       → 666
Directory  → 777

The execute bit is not automatically given to newly created regular files.

So with:

umask 022

you get:

File       → 644
Directory  → 755

3. Common umask values

| umask | New file | New directory |
| ----- | -------- | ------------- |
| `000` | `666`    | `777`         |
| `022` | `644`    | `755`         |
| `027` | `640`    | `750`         |
| `077` | `600`    | `700`         |


For example:

umask 077
touch secret.txt
mkdir secret_dir

Results approximately:

secret.txt   → 600
secret_dir   → 700

Meaning only the owner has access.

4. How to check umask
umask

Example:

0022

You can also use:

umask -S

to see a symbolic representation.

5. How to change it

For the current shell/session:

umask 027

Then:

touch file.txt
mkdir mydir

will typically produce:

file.txt → 640
mydir    → 750

To make it persistent, it can be configured in shell startup/environment configuration, depending on how the user/session is initialized.

⭐ Interview question: How does umask work?

Interviewer: What happens when you run touch file.txt with umask 022?

Answer:

A regular file starts with base permissions 666. The umask removes permissions specified by 022, resulting in 644, or rw-r--r--.

For:

mkdir test

the directory starts with 777, so:

777 - 022 → 755
⚠️ Important interview nuance

People often say:

"umask is subtracted from the default permission."

That's a useful interview shortcut, but technically it's better to say:

The umask masks/removes permission bits from the permissions requested by the application, subject to the filesystem/system rules.

For the common examples:

File:       666 with umask 022 → 644
Directory:  777 with umask 022 → 755

Think:

        Base permissions
              ↓
            umask
              ↓
      permissions removed
              ↓
       actual permissions
🧠 One-line interview answer

Umask is a process-level permission mask that controls which permission bits are cleared when new files and directories are created.