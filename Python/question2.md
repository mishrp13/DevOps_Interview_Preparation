
```
2.

Mutable vs Immutable — Interview Perspective

This is a very common Python interview topic, especially the mutable default argument bug.

The key idea is:

Mutable objects can be changed after creation; immutable objects cannot be changed in place.

1. Mutable vs Immutable
Mutable

A mutable object can be modified without creating a new object.

Common examples:

list
dict
set

Example:

x = [1, 2, 3]
x.append(4)

print(x)
# [1, 2, 3, 4]

The list itself was modified.

Immutable

An immutable object cannot be modified after it is created.

Common examples:

int
float
bool
str
tuple
frozenset
bytes

Example:

x = "hello"
x = x + " world"

Python doesn't modify the original "hello" string. It creates a new string object.

Conceptually:

"hello"
   ↓
new object
   ↓
"hello world"
2. Important interview question: Is a variable immutable?

Technically, objects are mutable or immutable, not variables.

For example:

x = 10

x is a reference/name pointing to an integer object.

If you do:

x = 20

you aren't modifying the integer 10. You're making x refer to another object.

A useful mental model:

x ───→ 10

x = 20

x ───→ 20
3. Why does immutability matter?

Consider:

a = "hello"
b = a

a = "world"

b remains:

"hello"

because strings are immutable.

With a mutable object:

a = [1, 2]
b = a

a.append(3)

print(b)

Output:

[1, 2, 3]

Why?

Because a and b reference the same list.

a ──┐
    ├──→ [1, 2]
b ──┘

a.append(3)

a ──┐
    ├──→ [1, 2, 3]
b ──┘
4. The Mutable Default Argument Bug ⭐

This is one of the most frequently asked Python interview questions.

Consider:

def add_item(item, items=[]):
    items.append(item)
    return items

Now:

print(add_item("a"))
print(add_item("b"))
print(add_item("c"))

Many beginners expect:

['a']
['b']
['c']

But the actual result is:

['a']
['a', 'b']
['a', 'b', 'c']
Why?

Because Python evaluates the default argument once, when the function is defined, not every time the function is called.

So this:

items=[]

creates one list.

That same list is reused across calls.

Conceptually:

Function definition
       │
       ▼
   items = []
       │
       ├── call 1 → append "a"
       │             ↓
       │          ["a"]
       │
       ├── call 2 → append "b"
       │             ↓
       │        ["a", "b"]
       │
       └── call 3 → append "c"
                     ↓
                  ["a","b","c"]
5. The correct solution ⭐

Use None as the default:

def add_item(item, items=None):
    if items is None:
        items = []

    items.append(item)
    return items

Now:

print(add_item("a"))
print(add_item("b"))
print(add_item("c"))

Output:

['a']
['b']
['c']

Each call creates a new list.

6. Why does None fix it?

None is immutable.

More importantly, the function doesn't use a mutable object as the default.

def add_item(item, items=None):

Every time the function executes:

if items is None:
    items = []

a new list is created.

Call 1 → new []
Call 2 → new []
Call 3 → new []
7. Interview question: Are default arguments evaluated every time?

No.

They are evaluated once when the function definition is executed.

For example:

def test(x=[]):
    ...

The default list is created once.

This is why mutable defaults can cause unexpected shared state.

8. Another example

Bad:

def add_user(name, users=[]):
    users.append(name)
    return users

Calling:

add_user("Alice")
add_user("Bob")

produces:

['Alice', 'Bob']

The second call sees the list from the first call.

Correct:

def add_user(name, users=None):
    if users is None:
        users = []

    users.append(name)
    return users
9. Is every default argument dangerous?

No.

Immutable defaults are generally fine:

def greet(name="Guest"):
    ...
def connect(port=8080):
    ...
def process(enabled=True):
    ...

The problem is specifically mutable objects whose state you modify.

Potentially problematic:

def f(x=[]):
def f(x={}):
def f(x=set()):
10. Important subtlety: +=

Interviewers sometimes use this to test whether you understand mutability.

x = [1, 2]
x += [3]

The list is modified in place.

But:

x = (1, 2)
x += (3,)

Since tuples are immutable, a new tuple is created and assigned to x.

11. is vs == — related interview concept

Because we're talking about objects, you should know this distinction:

==  → compares values
is  → compares object identity

Example:

a = [1, 2]
b = a

a == b   # True
a is b   # True

Because both refer to the same object.

But:

a = [1, 2]
b = [1, 2]

a == b   # True
a is b   # False

Same contents, different objects.

12. Quick comparison

| Type        | Mutable? | Example            |
| ----------- | -------- | ------------------ |
| `int`       | ❌        | `10`               |
| `float`     | ❌        | `3.14`             |
| `bool`      | ❌        | `True`             |
| `str`       | ❌        | `"hello"`          |
| `tuple`     | ❌        | `(1, 2)`           |
| `frozenset` | ❌        | `frozenset({1,2})` |
| `list`      | ✅        | `[1,2]`            |
| `dict`      | ✅        | `{"a":1}`          |
| `set`       | ✅        | `{1,2}`            |

⭐ Classic interview question

Interviewer: What is wrong with this function?

def append_value(value, result=[]):
    result.append(value)
    return result
Strong answer:

The default list is created only once when the function is defined. Since lists are mutable, every call that uses the default shares the same list, causing values from previous calls to persist. I would use None as the default and create a new list inside the function.

def append_value(value, result=None):
    if result is None:
        result = []

    result.append(value)
    return result
🧠 30-second interview answer

Mutable objects like lists, dictionaries, and sets can be modified in place, while immutable objects like strings, integers, and tuples cannot. Python evaluates function default arguments once at function definition time. Therefore, using a mutable object such as [] as a default argument can cause state to be shared across function calls. The standard solution is to use None as the default and create the mutable object inside the function.

One line to remember

Never use a mutable object as a default argument when you intend each function call to get a fresh object.