```

•$?, $$, $@, $#


In Bash, these are special variables used for scripting and automation.

- `$?` gives the exit status of the last command. Zero means success, and nonzero usually indicates failure.
- `$$` gives the process ID of the current shell.
- `"$@"` represents all arguments passed to the script while preserving each argument separately.
- `$#` gives the total number of arguments passed to the script.

In DevOps, I use `$?` to check command success, `$$` for temporary filenames, `"$@"` to pass arguments between scripts, and `$#` to validate input before running deployment or automation tasks.