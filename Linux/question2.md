```

2. 

What are inodes? Hard link vs soft link?

Answer:

Inodes

An inode (index node) is a data structure used by Unix/Linux filesystems to store metadata about a file.

An inode typically contains:

File type
File permissions
Owner and group
File size
Timestamps
Number of hard links
Pointers to the disk blocks containing the file's actual data

Important: The inode does not normally store the filename. The filename is stored in a directory entry, which maps the name → inode number.

You can see an inode number with:

ls -i file.txt


| Feature                | Hard Link            | Soft/Symbolic Link        |
| ---------------------- | -------------------- | ------------------------- |
| Points to              | Same **inode**       | Another **filename/path** |
| Inode                  | Same as original     | Different inode           |
| Data                   | Same underlying data | Points to original path   |
| If original is deleted | Still works          | Usually becomes broken    |
| Can cross filesystems? | ❌ No                 | ✅ Yes                     |
| Can link directories?  | Generally ❌          | ✅ Yes                     |
| `ls -l` shows          | Same file metadata   | `link → target`           |


Hard link
ln file.txt hard.txt

Both names refer to the same inode:

file.txt ──┐
           ├──> inode 1234 ──> data blocks
hard.txt ──┘

Deleting file.txt doesn't delete the data because hard.txt still references inode 1234.

The inode's link count decreases from 2 to 1.

Soft link / Symbolic link
ln -s file.txt soft.txt

Here:

soft.txt ──> inode 5678 ──> "file.txt" ──> inode 1234 ──> data

The symlink has its own inode and stores the path to the target.

If file.txt is deleted or moved, soft.txt can become a dangling/broken link.

Easy way to remember

Hard link = another name for the same inode.
Soft link = a pointer/path to another file.

Interview one-liner:
A hard link shares the same inode and data as the original file, whereas a soft link has its own inode and points to the original file by pathname.
