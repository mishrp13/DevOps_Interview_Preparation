

sqaures= [x*x for x in range(10)]
print(sqaures)


gen=(x*x for x in range(10**9))
# for value in gen:
#     print(value)

print(next(gen))
print(next(gen))


# def read_errors(path):
#     with open(path) as f:
#         for line in f:
#             if "ERROR" in line:
#                 yield line.strip()

# def process(line):
#     print("Found:", line)

# for line in read_errors("app.log"):
#     process(line)



def read_errors(path):
    with open(path) as f:
        for line in f:
            if "ERROR" in line:
                yield line.strip()

def process(line):
    print("Found", line)

for line in read_errors("app.log"):
    process(line)
