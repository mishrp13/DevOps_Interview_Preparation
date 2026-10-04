from collections import Counter

def top_ips(filename, n=10):

    counts = Counter()

    with open(filename) as file:

        for line in file:

            parts = line.split()

            if parts:
                ip = parts[0]
                counts[ip] += 1

    return counts.most_common(n)


for ip, count in top_ips("access.log"):
    print(f"{ip}: {count}")