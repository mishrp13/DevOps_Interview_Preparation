```
•__init__ vs __new__, __str__ vs __repr__  ?


For a DevOps Python interview, you don't need to go extremely deep into Python internals, but you should clearly understand these two pairs:

__new__ vs __init__ → object creation vs object initialization
__str__ vs __repr__ → human-readable vs developer/debug representation

1. __new__ vs __init__

Suppose you create an object:

server = Server("production")

Python roughly does:

        Server("production")
              ↓
          __new__()
       Create object
              ↓
          __init__()
     Initialize object
              ↓
         server object
__new__

__new__ is responsible for creating/allocating the object.

class Server:

    def __new__(cls, name):
        print("__new__ called")
        return super().__new__(cls)

    def __init__(self, name):
        print("__init__ called")
        self.name = name

When you run:

server = Server("production")

Output:

__new__ called
__init__ called

So:

__new__ creates the object.
__init__ initializes the already-created object.

2. Why is __new__ rarely used?

In normal DevOps automation, you'll usually write:

class Server:

    def __init__(self, name):
        self.name = name

You generally don't need to override __new__.

__new__ becomes useful for things like:

Singleton patterns
Immutable objects
Custom object creation
Subclassing certain built-in types
Controlling whether a new object is created

For a DevOps interview, knowing why it exists is more important than writing complex __new__ implementations.

3. Important interview trick

Consider:

class Server:

    def __new__(cls):
        print("Creating object")
        return super().__new__(cls)

    def __init__(self):
        print("Initializing object")

When:

server = Server()

The order is:

Creating object
       ↓
Initializing object

So if interviewer asks:

"Which one runs first, __new__ or __init__?"

Answer:

__new__ runs first, then __init__.

4. What if __new__ doesn't return an object?

This is a more advanced interview question.

Normally:

def __new__(cls):
    return super().__new__(cls)

If __new__ doesn't return an instance of the class, __init__ may not be called.

For example:

class Server:

    def __new__(cls):
        print("new")
        return None

    def __init__(self):
        print("init")

Then:

server = Server()

You won't get the normal initialization flow because an object wasn't created/returned.

For most DevOps interviews, just remember:

__new__ controls object creation; __init__ initializes the created object.

5. Now __str__ vs __repr__

This is another very common interview question.

Suppose you have:

class Server:

    def __init__(self, name, environment):
        self.name = name
        self.environment = environment

Create:

server = Server("web01", "production")

If you do:

print(server)

you'll get something ugly like:

<__main__.Server object at 0x000001...>

That's where __str__ comes in.

6. __str__ = human-readable

Define:

class Server:

    def __init__(self, name, environment):
        self.name = name
        self.environment = environment

    def __str__(self):
        return f"{self.name} ({self.environment})"

Now:

server = Server("web01", "production")

print(server)

Output:

web01 (production)

So:

__str__ gives a user-friendly/human-readable representation of an object.

For DevOps, imagine logging:

print(server)

You'd want:

web01 (production)

rather than:

<__main__.Server object at 0x000001...>
7. __repr__ = developer/debug representation

Now add __repr__:

class Server:

    def __init__(self, name, environment):
        self.name = name
        self.environment = environment

    def __str__(self):
        return f"{self.name} ({self.environment})"

    def __repr__(self):
        return (
            f"Server(name={self.name!r}, "
            f"environment={self.environment!r})"
        )

Now:

server = Server("web01", "production")

print(server)

gives:

web01 (production)

But:

print(repr(server))

gives:

Server(name='web01', environment='production')

So:

__str__ → readable for humans
__repr__ → useful for developers/debugging

8. The important difference

Remember this table:

| Method     | Purpose                        | Typical use                  |
| ---------- | ------------------------------ | ---------------------------- |
| `__new__`  | Create object                  | Advanced object creation     |
| `__init__` | Initialize object              | Set attributes/configuration |
| `__str__`  | Human-readable output          | `print(obj)`                 |
| `__repr__` | Developer/debug representation | `repr(obj)`, debugging       |


The easiest way to remember:

__new__  → NEW object
__init__ → INITIALIZE object

__str__  → STRing for humans
__repr__ → REPresentation for developers
9. DevOps example

Imagine you're writing a Python automation tool that manages servers.

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

Now:

server = Server(
    "web01",
    "production",
    "10.0.1.20"
)

For a deployment log:

print(server)

You get:

web01 [production]

Nice and clean.

For debugging:

print(repr(server))

You get:

Server(hostname='web01', environment='production', ip='10.0.1.20')

Much more useful when troubleshooting.

10. Why repr() matters in DevOps

This is particularly useful when you're dealing with lists of objects.

Suppose:

servers = [
    Server("web01", "production", "10.0.1.20"),
    Server("web02", "production", "10.0.1.21")
]

If __repr__ is implemented properly:

print(servers)

can give something like:

[
    Server(hostname='web01', environment='production', ip='10.0.1.20'),
    Server(hostname='web02', environment='production', ip='10.0.1.21')
]

This is much easier to debug than:

[<Server object at 0x...>, <Server object at 0x...>]

This matters when troubleshooting automation scripts, inventory systems, deployment objects, configuration objects, etc.

11. Important interview question: What happens if only __repr__ exists?

Suppose:

class Server:

    def __repr__(self):
        return "Server(web01)"

Then:

server = Server()

print(server)

will generally use __repr__ as a fallback when __str__ isn't defined.

So:

print(obj)

looks for:

__str__
   ↓
if unavailable
   ↓
__repr__

But don't say that __str__ and __repr__ are exactly the same—they have different intended purposes.

12. Interview scenario
Interviewer:

"What's the difference between __str__ and __repr__?"

Good answer:

"__str__ is intended to provide a human-readable representation of an object, typically for users or logs. __repr__ is intended to provide an unambiguous developer-oriented representation, mainly useful for debugging. For example, I might use __str__ to display web01 [production], while __repr__ could display Server(hostname='web01', environment='production', ip='10.0.1.20')."

That's a strong answer.

13. Interview scenario: __new__ vs __init__
Interviewer:

"What's the difference between __new__ and __init__?"

Answer:

"__new__ is responsible for creating and returning a new instance, while __init__ initializes the instance after it's been created. __new__ runs first. In normal Python classes, I usually only need __init__; I would override __new__ for special object-creation requirements such as immutable types or controlling instance creation."

⭐ What to memorize

For your DevOps interview, I'd memorize these four lines:

__new__  → creates the object
__init__ → initializes the object

__str__  → human-readable representation
__repr__ → developer/debug representation

And remember the lifecycle:

Server(...)
   ↓
__new__()
   ↓
object created
   ↓
__init__()
   ↓
object initialized

Then when displaying it:

print(server)
      ↓
   __str__()

repr(server)
      ↓
   __repr__()

These four methods are common Python interview questions, but for a DevOps role, focus on knowing what they do, when they're called, and one practical automation example, rather than getting deep into Python object-model internals.