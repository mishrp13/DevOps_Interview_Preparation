def get_errors(file_name):
    with open(file_name) as f:
        for line in f:
            print("Reading line...")
            
            if "ERROR" in line:
                print("Found ERROR, yielding it...")
                yield line

for error in get_errors("application.log"):
    print("Consumer received:", error)