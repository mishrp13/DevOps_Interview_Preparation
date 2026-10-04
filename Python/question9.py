class Server:

    def __init__(self, hostname, environment, ip):
        self.hostname = hostname
        self.environment = environment
        self.ip = ip

    def __str__(self):
        return f"{self.hostname} [{self.environment}]"

    def __repr__(self):
        return (
            f"Server(hostname={self.hostname!r}, "
            f"environment={self.environment!r}, "
            f"ip={self.ip!r})"
        )



server = Server(
    "web01",
    "production",
    "10.0.1.20"
)

print(server)

print(repr(server))