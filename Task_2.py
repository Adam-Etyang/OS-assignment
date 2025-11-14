processes = [
    {"pid": "P1", "arrival": 3, "burst": 1},
    {"pid": "P2", "arrival": 1, "burst": 4},
    {"pid": "P3", "arrival": 4, "burst": 2},
    {"pid": "P4", "arrival": 0, "burst": 6},
    {"pid": "P5", "arrival": 2, "burst": 3},
]

for p in processes:
    p["remaining"] = p["burst"]

time = 0
completed = 0
n = len(processes)

completion = {}
turnaround = {}
waiting = {}

while completed < n:
    ready = [p for p in processes if p["arrival"] <= time and p["remaining"] > 0]

    if not ready:
        time += 1
        continue

    current = min(ready, key=lambda x: x["remaining"])
    current["remaining"] -= 1
    time += 1

    if current["remaining"] == 0:
        completed += 1
        completion[current["pid"]] = time

for p in processes:
    pid = p["pid"]
    arrival = p["arrival"]
    burst = p["burst"]

    tat = completion[pid] - arrival
    wt = tat - burst

    turnaround[pid] = tat
    waiting[pid] = wt

print("PID\tAT\tBT\tCT\tTAT\tWT")
for p in processes:
    pid = p["pid"]
    print(f"{pid}\t{p['arrival']}\t{p['burst']}\t{completion[pid]}\t{turnaround[pid]}\t{waiting[pid]}")

avg_tat = sum(turnaround.values()) / n
avg_wt = sum(waiting.values()) / n

print("\nAverage Turnaround Time:", avg_tat)
print("Average Waiting Time:", avg_wt)
