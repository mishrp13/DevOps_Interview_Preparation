```

•systemd: how do you start, stop and enable a service? How do you write a unit file? How do you read logs with journalctl?

For a DevOps interview, systemd is important because it's the service manager used by many modern Linux distributions. You should be comfortable with starting/stopping services, enabling them at boot, writing a basic unit file, and troubleshooting with journalctl.

A good way to remember it:

systemctl → manage services
journalctl → read service logs
1. What is systemd?

systemd is the system and service manager for Linux.

It can:

start services
stop services
restart services
enable services at boot
monitor service state
manage dependencies
collect/manage logs through the journal

For example:

Linux boots
    ↓
systemd
    ↓
Starts configured services
    ↓
nginx / ssh / docker / application...
2. Start a service

Use:

sudo systemctl start nginx

This starts nginx now.

Important:

start does not mean the service will automatically start after the next reboot.

3. Stop a service
sudo systemctl stop nginx

This stops it now.

4. Restart a service
sudo systemctl restart nginx

Useful after changing configuration.

For example:

sudo systemctl restart nginx
5. Reload a service

You may also see:

sudo systemctl reload nginx

The difference:

restart
   ↓
Stop + start service

reload
   ↓
Ask service to reload configuration
without fully restarting it

Whether reload is supported depends on the service.

For example, after changing an Nginx configuration:

sudo nginx -t
sudo systemctl reload nginx

A good DevOps practice is to validate configuration before reloading/restarting when the service provides a validation command.

6. Check service status

Very important for troubleshooting:

systemctl status nginx

You might see:

● nginx.service - A high performance web server
     Loaded: loaded (...)
     Active: active (running)
   Main PID: 1234 (nginx)
      Tasks: 5
     Memory: 8.5M

Pay attention to:

Active: active (running)
Main PID: 1234

If it failed:

Active: failed

You can then investigate logs.

7. Enable a service at boot

This is where interviewers often test the difference between start and enable.

sudo systemctl enable nginx

enable configures the service to start automatically during boot, according to its unit configuration.

It does not necessarily start the service immediately.

So:

start
  → start it NOW

enable
  → start it automatically at BOOT

You can do both:

sudo systemctl enable --now nginx

This means:

Enable it for boot and start it now.

8. Disable a service
sudo systemctl disable nginx

This prevents it from being automatically started through its normal boot enablement.

It does not necessarily stop an already-running service.

So:

disable
   ↓
Don't automatically start at boot

stop
   ↓
Stop it now
⭐ Important commands to remember
systemctl start <service>
systemctl stop <service>
systemctl restart <service>
systemctl reload <service>

systemctl status <service>

systemctl enable <service>
systemctl disable <service>

systemctl enable --now <service>
9. How do you write a systemd unit file?

This is a very useful DevOps interview topic.

Suppose you have your own Python application:

/opt/myapp/app.py

and you want systemd to manage it.

Create a unit file, commonly under:

/etc/systemd/system/myapp.service

Example:

[Unit]
Description=My Python Application
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/python3 /opt/myapp/app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target

Let's break this down.

10. [Unit]
[Unit]
Description=My Python Application
After=network.target
Description

Human-readable description:

Description=My Python Application
After

Controls ordering.

After=network.target

This says:

Start this unit after network.target has been reached.

Important interview nuance:

After= controls ordering; it does not by itself create a dependency that causes the other unit to be started.

11. [Service]

This is where you define how the application runs.

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/python3 /opt/myapp/app.py
Restart=on-failure
User
User=myapp

Run the application as the myapp user instead of root.

This is generally preferable for application services when root privileges aren't required.

WorkingDirectory
WorkingDirectory=/opt/myapp

Sets the working directory for the service.

ExecStart
ExecStart=/usr/bin/python3 /opt/myapp/app.py

Defines the command systemd starts.

Restart
Restart=on-failure

Tells systemd to restart the service when it exits unsuccessfully.

Other restart policies exist, such as:

Restart=always

but choose the policy based on the application's behavior.

12. [Install]
[Install]
WantedBy=multi-user.target

This is commonly used with:

systemctl enable myapp

It tells systemd how the service participates in the boot target when enabled.

13. After creating a unit file

This is very important.

If you create or modify a unit file, run:

sudo systemctl daemon-reload

Why?

Because systemd needs to reload its unit configuration.

Then:

sudo systemctl start myapp

Check:

sudo systemctl status myapp

Enable at boot:

sudo systemctl enable myapp

Or:

sudo systemctl enable --now myapp
14. Reading logs with journalctl

journalctl is used to query the systemd journal.

For a specific service:

journalctl -u myapp

This is extremely useful when:

systemctl status myapp

shows:

Active: failed

You can then inspect the service's logs.

Show recent logs
journalctl -u myapp
Show logs from the current boot
journalctl -u myapp -b
Follow logs live

This is very useful during deployments:

journalctl -u myapp -f

Similar idea to:

tail -f

You're watching new log entries as they arrive.

Show only recent logs

For example:

journalctl -u myapp --since "10 minutes ago"

Or:

journalctl -u myapp --since today
15. DevOps troubleshooting scenario ⭐

Imagine you deployed:

sudo systemctl restart myapp

But:

systemctl status myapp

shows:

Active: failed

Don't immediately start changing random things.

Step 1 — Check status
systemctl status myapp
Step 2 — Read logs
journalctl -u myapp -n 100

For live troubleshooting:

journalctl -u myapp -f

You might find:

ModuleNotFoundError: No module named 'flask'

or:

Address already in use

or:

Permission denied

Now you have a concrete error to investigate.

16. Useful journalctl commands
Command	Purpose
| Command                             | Purpose                |
| ----------------------------------- | ---------------------- |
| `journalctl -u nginx`               | Logs for nginx         |
| `journalctl -u nginx -f`            | Follow nginx logs      |
| `journalctl -u nginx -n 100`        | Last 100 entries       |
| `journalctl -u nginx -b`            | Logs from current boot |
| `journalctl -u nginx --since today` | Today's logs           |
| `journalctl -b`                     | Logs from current boot |
| `journalctl -p err`                 | Error-priority entries |

17. Complete DevOps workflow

Suppose you're deploying a custom application.

Create unit:
sudo vi /etc/systemd/system/myapp.service

Put:

[Unit]
Description=My Python Application
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/python3 /opt/myapp/app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target

Then:

sudo systemctl daemon-reload

Start:

sudo systemctl start myapp

Check:

sudo systemctl status myapp

Enable at boot:

sudo systemctl enable myapp

Or simply:

sudo systemctl enable --now myapp

If something goes wrong:

journalctl -u myapp -n 100

And for live logs:

journalctl -u myapp -f
⭐ Interview answer to memorize

If the interviewer asks:

"How do you manage a service using systemd?"

You can answer:

"I use systemctl to manage systemd services. For example, systemctl start starts a service, stop stops it, restart restarts it, and status checks its current state. enable configures the service to start at boot, while enable --now both enables and starts it immediately. For a custom application, I can create a unit file under /etc/systemd/system/ with sections such as [Unit], [Service], and [Install]. After creating or modifying the unit file, I run systemctl daemon-reload. For troubleshooting, I use journalctl -u <service> to inspect its logs and journalctl -u <service> -f to follow them live."

🧠 The 4 commands I'd memorize first
systemctl status myapp
systemctl restart myapp
systemctl enable myapp
journalctl -u myapp -f

And for a custom service, remember the sequence:

Create .service file
       ↓
daemon-reload
       ↓
start
       ↓
status
       ↓
enable
       ↓
journalctl

That sequence is very useful for real-world DevOps troubleshooting as well as interviews.