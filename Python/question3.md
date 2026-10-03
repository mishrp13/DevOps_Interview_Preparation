```

•`is` vs `==`?


In a DevOps interview, this usually comes up in the context of Python scripting/automation, especially when writing scripts for CI/CD, infrastructure automation, monitoring, etc.

is vs == in Python
Operator	Checks	Example
==	Value equality	a == b → do they have the same value?
is	Object identity	a is b → are they the exact same object in memory?
Example
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)   # True
print(a is b)   # False

Why?

a and b contain the same values, so a == b is True.
But they are two different list objects, so a is b is False.

Think of it as:

== → "Do these things have the same contents?"
is → "Are these literally the same object?"

A common interview example
x = None

if x is None:
    print("No value")

Use is None, not:

if x == None:

None is a singleton in Python, so the conventional and correct identity check is:

x is None

Similarly:

if result is not None:
    ...
Important interview trap

Don't say:

"is compares memory addresses."

That's an oversimplification.

A better interview answer is:

"== checks whether two objects are equal in value, while is checks whether they are the same object (object identity). In Python, is is commonly used for singleton values such as None, True, and False, while == is used for normal value comparisons."

DevOps-oriented example

Suppose you're checking the result of a command:

result = None

if result is None:
    print("Command did not return a result")

Or comparing command output:

status = "failed"

if status == "failed":
    print("Deployment failed")

Here == is appropriate because you're comparing the value of status.

Easy rule for the interview:

is  → identity → same object?
==  → equality → same value?

If the interviewer asks a follow-up, be ready for Python's id(), string/integer interning, and why is can sometimes appear to work with small integers/strings—that's a common trick question.