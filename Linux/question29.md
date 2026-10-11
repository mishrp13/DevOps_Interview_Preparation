```
•Replace a string in all files in a directory

In a Linux DevOps interview, “How do you replace a string in all files in a directory?” can be answered using grep to find files and sed to replace text.
1. One-command solution
grep -rl 'old_string' /path/to/directory | xargs sed -i 's/old_string/new_string/g'


Example: Replace localhost with production-server in files under /etc/myapp/.
grep -rl 'localhost' /etc/myapp/ | xargs sed -i 's/localhost/production-server/g'



2. Explain each command

Command	          Meaning
grep -r	          Search recursively through directories
-l	              Print filenames containing the string
xargs             Pass the filenames to another command
sed -i                Edit files in place
s/old/new/g           Replace every occurrence of old with new on each line

What does g mean? It replaces all occurrences on each line, rather than just the first occurrence

3. Safer approach for DevOps
First, check which files contain the string:
grep -rl 'localhost' /etc/myapp/


Then make backups while replacing the string:
grep -rlZ 'localhost' /etc/myapp/ | xargs -0 -r sed -i.bak 's/localhost/production-server/g'


- -Z and -0 safely handle filenames containing spaces or unusual characters.
- -r on xargs skips running sed if no files are found.
- -i.bak creates a backup of each modified file with a .bak suffix.
Important: Review the target directory before running replacement commands, especially in production. A broad replacement can modify configuration values you did not intend to change.



4. Interview-ready answer
“I use grep -rl to find all files containing the target string, then pipe those filenames to sed -i to replace the text in place. I use a backup option such as sed -i.bak when working on important configuration files, and I verify the changes afterward.”
Useful follow-up: If the interviewer asks to replace the string only in .conf files, you can use:
find /etc/myapp -type f -name '*.conf' -exec sed -i.bak 's/localhost/production-server/g' {} +


This searches only regular files ending in .conf and replaces the string in those files.