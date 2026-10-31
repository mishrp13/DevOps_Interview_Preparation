
import os
import hashlib

def get_file_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

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
