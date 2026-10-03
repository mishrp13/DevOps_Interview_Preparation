```
1. 
List vs tuple vs set vs dict: differences and when to use each?

List vs Tuple vs Set vs Dictionary — Interview Perspective

These are the 4 most common built-in collection types in Python. The key difference is how they store data, whether order/duplicates are allowed, mutability, and how you access elements.

1. Quick comparison
| Feature         | List                | Tuple            | Set                          | Dictionary                      |
| --------------- | ------------------- | ---------------- | ---------------------------- | ------------------------------- |
| Syntax          | `[ ]`               | `( )`            | `{ }`                        | `{key: value}`                  |
| Ordered         | Yes                 | Yes              | No meaningful indexing order | Insertion-ordered (Python 3.7+) |
| Mutable         | ✅ Yes               | ❌ No             | ✅ Yes                        | ✅ Yes                           |
| Duplicates      | ✅ Allowed           | ✅ Allowed        | ❌ Not allowed                | Keys ❌, values ✅                |
| Indexing        | ✅ Yes               | ✅ Yes            | ❌ No                         | By key                          |
| Key-value pairs | ❌                   | ❌                | ❌                            | ✅                               |
| Main use        | Collection of items | Fixed collection | Unique items                 | Mapping/lookup                  |
| Typical lookup  | `O(n)`              | `O(n)`           | Average `O(1)`               | Average `O(1)`                  |

2. List

A list is an ordered, mutable collection that allows duplicate values.

fruits = ["apple", "banana", "apple"]

print(fruits[0])
# apple

fruits.append("orange")
fruits[1] = "mango"


Characteristics
Ordered
Mutable
Allows duplicates
Supports indexing and slicing
Can contain different data types
data = [10, "hello", 3.14, True]
When to use List?

Use a list when:

You need an ordered collection and may need to modify it.

Examples:

servers = ["server1", "server2", "server3"]

servers.append("server4")
servers.remove("server2")
Interview point
numbers = [10, 20, 30]
print(numbers[1])   # 20

Lists support index-based access.

3. Tuple

A tuple is an ordered but immutable collection.

coordinates = (10, 20)

print(coordinates[0])
# 10

You cannot modify it:

coordinates[0] = 100

This gives:

TypeError
When to use Tuple?

Use a tuple when:

The collection should not change after creation.

Example:

server_info = ("web01", "192.168.1.10", 80)

You can also use tuples for returning multiple values:

def get_user():
    return "alice", 1001

name, uid = get_user()
Important interview point

Because tuples are immutable, they can be used as dictionary keys if all their elements are hashable.

locations = {
    (10, 20): "Point A",
    (30, 40): "Point B"
}

A list cannot be a dictionary key:

# TypeError
my_dict = {[1, 2]: "value"}
4. Set

A set is a mutable collection of unique elements.

numbers = {1, 2, 3, 3, 4}

print(numbers)
# {1, 2, 3, 4}

Duplicates are automatically removed.

When to use Set?

Use a set when:

You care about uniqueness or fast membership testing rather than indexing.

Example:

servers = {"web01", "web02", "web03"}

if "web02" in servers:
    print("Server exists")

Set operations are also useful:

a = {1, 2, 3}
b = {3, 4, 5}

print(a & b)   # intersection
print(a | b)   # union
print(a - b)   # difference

Output:

{3}
{1, 2, 3, 4, 5}
{1, 2}
Interview point

A set does not support indexing:

numbers = {10, 20, 30}

numbers[0]

This raises:

TypeError
5. Dictionary

A dictionary stores data as key-value pairs.

user = {
    "name": "Alice",
    "uid": 1001,
    "role": "admin"
}

Access values using keys:

print(user["name"])
# Alice

Modify:

user["role"] = "developer"

Add:

user["shell"] = "/bin/bash"
When to use Dictionary?

Use a dictionary when:

You need to associate a key with a value or perform fast key-based lookups.

Example:

users = {
    "alice": 1001,
    "bob": 1002,
    "john": 1003
}

print(users["alice"])
# 1001

This is much more appropriate than searching through a list of users.

6. The easiest way to remember

Think about what you need:

Need ordered + changeable?
        ↓
      LIST

Need ordered + fixed?
        ↓
     TUPLE

Need unique values?
        ↓
      SET

Need key → value mapping?
        ↓
    DICTIONARY
7. Important interview trap: {}

A common interview question:

What is the type of {}?
x = {}

print(type(x))

Output:

<class 'dict'>

An empty set is created using:

x = set()

Not:

x = {}
8. List vs Tuple — common interview question
List	Tuple
Mutable	Immutable
[]	()
Can be modified	Cannot be modified
Generally used for dynamic collections	Generally used for fixed collections
Not hashable	Can be hashable if elements are hashable

Example:

my_list = [1, 2, 3]
my_list.append(4)

Works.

my_tuple = (1, 2, 3)
my_tuple.append(4)

Fails because tuples don't have append().

9. List vs Set

Suppose you have:

users = ["alice", "bob", "alice", "john"]

If you need to preserve duplicates/order:

users

Use a list.

If you only need unique users:

unique_users = set(users)

print(unique_users)

Use a set.

For membership checks:

if "alice" in users:
    ...

A set is generally preferred for repeated membership testing because average lookup is O(1), whereas list membership is O(n).

10. Set vs Dictionary

This is another common interview question.

Set

Stores only values:

servers = {"web01", "web02", "web03"}
Dictionary

Stores key-value pairs:

servers = {
    "web01": "10.0.0.1",
    "web02": "10.0.0.2"
}

Think:

SET  → unique values

DICT → key → value
11. Time complexity — interview perspective

Typical average-case behavior:

Operation	List	Tuple	Set	Dict
Index access	O(1)	O(1)	❌	—
Search/membership	O(n)	O(n)	O(1) avg	O(1) avg by key
Append	O(1) amortized	❌	O(1) avg	O(1) avg
Delete	O(n)	❌	O(1) avg	O(1) avg

For interviews, remember:

List/Tuple → sequence-based
Set/Dict → hash-based lookup

The O(1) for sets/dictionaries is average-case, not an unconditional guarantee.

12. Practical examples
List — task queue
tasks = ["backup", "deploy", "restart"]
tasks.append("monitor")
Tuple — fixed configuration
db_config = ("localhost", 5432, "mydb")
Set — unique IPs
unique_ips = {"10.0.0.1", "10.0.0.2", "10.0.0.1"}

Result:

{"10.0.0.1", "10.0.0.2"}
Dictionary — user information
user = {
    "username": "alice",
    "uid": 1001,
    "shell": "/bin/bash"
}
13. Most important interview questions
Q1. Which collection allows duplicates?

List and tuple.

Q2. Which collection stores only unique values?

Set.

Q3. Which collection stores key-value pairs?

Dictionary.

Q4. Which collections are mutable?

List, set, and dictionary.

Tuple is immutable.

Q5. Can a list be a dictionary key?

No. Lists are mutable and therefore unhashable.

Q6. Can a tuple be a dictionary key?

Yes, if all elements inside the tuple are hashable.

Q7. Which is faster for membership testing: list or set?

Generally set, because average membership lookup is O(1) versus O(n) for a list.

Q8. Does a set support indexing?

No.

s = {10, 20, 30}
s[0]       # TypeError
One-line interview answer

“A list is an ordered mutable collection that allows duplicates, a tuple is an ordered immutable collection, a set stores unique values with fast membership lookup, and a dictionary stores key-value pairs for fast key-based lookup.”

-----------------------------------------------------------------------------------------------------------

