```
Find duplicate files in a directory (hashing)?


import os
import hashlib

def get_file_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicates(directory):
    hashes = {}

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            try:
                file_hash = get_file_hash(file_path)

                if file_hash in hashes:
                    print("Duplicate Found:")
                    print("Original:", hashes[file_hash])
                    print("Duplicate:", file_path)
                    print("-------------------")
                else:
                    hashes[file_hash] = file_path

            except (OSError, PermissionError) as e:
                print("Error:", e)


find_duplicates("/home/ubuntu/files")


Example Directory
/home/ubuntu/files/
    file1.txt  → Hello DevOps
    file2.txt  → Hello Python
    file3.txt  → Hello DevOps
    file4.txt  → Hello DevOps


Expected Output
Duplicate Found:
Original: /home/ubuntu/files/file1.txt
Duplicate: /home/ubuntu/files/file3.txt
-------------------
Duplicate Found:
Original: /home/ubuntu/files/file1.txt
Duplicate: /home/ubuntu/files/file4.txt   


Explanation for Interview
1. os.walk() – Recursively scans all files and subdirectories.
2. hashlib.sha256() – Generates a SHA-256 hash based on file contents.
3. open(file_path, "rb") – Reads files in binary mode.
4. read(4096) – Reads files in 4 KB chunks, avoiding loading entire files into memory.
5. Dictionary (hashes) – Stores each hash with its first file path.
6. Hash comparison – If a hash already exists, the file is reported as a duplicate.


Question	                    Answer
Why use SHA-256?	  It provides a strong content fingerprint with an extremely low collision probability.
Why not compare filenames?	           Different filenames can contain identical data.
Why use os.walk()?	                   To recursively scan directories.
Why read in chunks?	                   To handle large files efficiently.
Does the script delete duplicates?	   No, it only identifies them.
What is the time complexity?	    O(N + B), where N is the number of files and B is the total bytes read.


Important: Matching SHA-256 hashes are strong evidence of identical content, but not mathematical proof. For strict verification, compare file bytes before deleting anything.