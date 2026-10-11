```
•What is a cron job? How do you write one that runs every 15 minutes?

A cron job is a Linux utility used to schedule commands or scripts to run automatically at specific times or intervals.

To run a script every 15 minutes, I add this entry using `crontab -e`:

`*/15 * * * * /path/to/script.sh`

The `*/15` means every 15 minutes, and the remaining four asterisks mean every hour, every day of the month, every month, and every day of the week.

I verify the job using `crontab -l`. In a DevOps environment, I also use absolute paths, ensure the script has the correct permissions, and redirect output and errors to a log file for troubleshooting.


*/15 — every 15 minutes.

First * — every hour.

Second * — every day of the month.

Third * — every month.

Fourth * — every day of the week.


Minute -> Hour -> Day of month -> Month -> Day of week