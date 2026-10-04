```
3.  File permissions: chmod 755, chown, setuid, setgid, sticky bit?

Ans:

1. chmod 755

chmod = change file permissions.

Linux permissions are divided into:

        Owner   Group   Others
         rwx     rwx     rwx
         7       5       5

So:

chmod 755 script.sh

means:

7 = rwx = read + write + execute
5 = r-x = read + execute
5 = r-x = read + execute

Therefore:

-rwxr-xr-x
Why numbers?
Permission	Value
Read (r)	4
Write (w)	2
Execute (x)	1

So:

7 = 4 + 2 + 1 = rwx
6 = 4 + 2     = rw-
5 = 4 + 1     = r-x
4 = 4         = r--
Common examples
chmod 644 file.txt
# owner: rw-
# group: r--
# others: r--

chmod 755 script.sh
# owner: rwx
# group: r-x
# others: r-x

chmod 700 secret.sh
# owner: rwx
# group: ---
# others: ---

Interview answer:

chmod 755 gives the owner read/write/execute permissions and gives the group and others read/execute permissions.

2. chown

chown = change ownership.

Every file has an owner and a group.

Check it with:

ls -l file.txt

Example:

-rw-r--r--  alice developers file.txt

Here:

alice       → owner
developers  → group
Change owner
sudo chown bob file.txt

Now bob owns the file.

Change owner and group
sudo chown bob:developers file.txt
Recursively
sudo chown -R bob:developers /app

-R means apply recursively.

chmod vs chown

This is a common interview question:

chmod changes permissions; chown changes ownership.

chmod → Who can read/write/execute?
chown → Who owns the file?
3. setuid

setuid = Set User ID

It is a special permission used mainly on executables.

Normally, when you execute a program:

your user
   ↓
program
   ↓
runs with your privileges

With setuid:

your user
   ↓
setuid program
   ↓
runs with owner's effective privileges

For example, historically /usr/bin/passwd uses setuid because changing your password requires modifying protected files.

You may see:

-rwsr-xr-x

Notice the s where the owner's execute permission normally appears.

Set setuid
chmod u+s program

or numerically:

chmod 4755 program

The leading 4 represents setuid.

Interview answer

Setuid causes an executable to run with the effective privileges of the file's owner rather than the privileges of the user executing it.

Security point: Setuid programs must be carefully controlled because a vulnerable setuid-root program can potentially allow privilege escalation.

4. setgid

setgid = Set Group ID

It has two important uses.

On executable files

Similar to setuid, a setgid executable runs with the file owner's group privileges.

You might see:

-rwxr-sr-x

The s appears in the group's execute position.

Set it with:

chmod g+s program

or:

chmod 2755 program

The leading 2 represents setgid.

On directories — very important for interviews

When setgid is applied to a directory, new files/directories inherit the directory's group.

Example:

chmod g+s /shared

Suppose:

/shared
    group = developers

Alice creates:

/shared/a.txt

The new file will inherit the developers group rather than necessarily using Alice's primary group.

This is extremely useful for shared project directories.

Interview answer

On an executable, setgid makes it run with the file's group privileges. On a directory, it causes newly created files and directories to inherit the directory's group.

5. Sticky bit

The sticky bit is mainly used on directories.

It means:

Users can create files in the directory, but generally can delete/rename only files they own (or if they have appropriate privileged access).

Classic example:

/tmp

/tmp is commonly:

drwxrwxrwt

Notice the t at the end.

Without the sticky bit, if users have write permission on a shared directory, one user could potentially delete another user's files.

Set sticky bit
chmod +t /shared

or numerically:

chmod 1777 /shared

The leading 1 represents the sticky bit.

| Special permission | Numeric value | Symbol | Main purpose                                                      |
| ------------------ | ------------: | ------ | ----------------------------------------------------------------- |
| **setuid**         |           `4` | `s`    | Executable runs with owner's privileges                           |
| **setgid**         |           `2` | `s`    | Executable runs with group's privileges; directory inherits group |
| **sticky bit**     |           `1` | `t`    | Directory users generally delete/rename only their own files      |


Therefore:

4755 → setuid + 755
2755 → setgid + 755
1777 → sticky bit + 777
⭐ Interview scenario

Interviewer: Why does /tmp usually have 1777 permissions?

Answer:

/tmp needs to be writable by all users, so it has 777 permissions. The sticky bit (1) prevents one normal user from deleting or renaming another user's files. Therefore, 1777 means rwxrwxrwx plus the sticky bit.

⭐ Another common question

Interviewer: What's the difference between 755 and 4755?

755  → rwxr-xr-x
4755 → rwsr-xr-x

4755 has setuid enabled because of the leading 4.

Quick interview cheat sheet
chmod → change permissions
chown → change owner/group

r = 4
w = 2
x = 1

755 → owner rwx, group r-x, others r-x
644 → owner rw-, group r--, others r--

Special bits:

4xxx → setuid
2xxx → setgid
1xxx → sticky bit

setuid → executable gets owner's effective privileges
setgid → executable gets group's privileges
          directory → new files inherit directory's group
sticky → shared directory → users generally delete their own files

If you're preparing for a Linux/DevOps interview, the next closely related topics are umask, ACLs (getfacl/setfacl), effective UID/GID, and the difference between rwx permissions on files vs directories

-------------------