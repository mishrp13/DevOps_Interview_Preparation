```
•Explain >, >>, 2>&1, | and tee

In Linux, we use redirection and pipes to manage command output and logs.

- **`>`** redirects output to a file and overwrites existing content.
- **`>>`** appends output to a file without deleting existing content.
- **`2>&1`** redirects error output to the same destination as standard output.
- **`|`** passes the output of one command as input to another command.
- **`tee`** displays output on the terminal and saves it to a file at the same time.

For example, during a deployment, I use:

`./deploy.sh 2>&1 | tee -a deploy.log`

This displays both normal output and errors on the terminal while appending them to `deploy.log`. It helps me monitor the deployment in real time and troubleshoot failures later.