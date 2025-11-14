class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.completion = 0
        self.turnaround = 0
        self.waiting = 0
        self.start_time = -1


def preemptive_priority_scheduling(processes):
    n = len(processes)
    current_time = 0
    completed = 0
    gantt_chart = []

    # Find the maximum time needed
    max_time = max(p.arrival for p in processes) + sum(p.burst for p in processes)

    print("\n=== PREEMPTIVE PRIORITY SCHEDULING ===\n")
    print("Process Execution Timeline:")
    print("-" * 60)

    prev_process = None

    while completed < n:
        # Find all processes that have arrived and are not completed
        available = [p for p in processes if p.arrival <= current_time and p.remaining > 0]

        if not available:
            # No process available, CPU is idle
            current_time += 1
            continue

        # Select process with highest priority (higher number = higher priority)
        # If priorities are equal, select the one that arrived first (FCFS)
        current_process = max(available, key=lambda p: (p.priority, -p.arrival))

        # Record start time if this is the first time the process runs
        if current_process.start_time == -1:
            current_process.start_time = current_time

        # Execute for 1 time unit
        current_process.remaining -= 1

        # Add to Gantt chart
        if prev_process != current_process.pid:
            gantt_chart.append((current_process.pid, current_time))
            prev_process = current_process.pid

        current_time += 1

        # Check if process is completed
        if current_process.remaining == 0:
            completed += 1
            current_process.completion = current_time
            current_process.turnaround = current_process.completion - current_process.arrival
            current_process.waiting = current_process.turnaround - current_process.burst

    # Display Gantt Chart
    print("\nGantt Chart:")
    print("|", end="")
    for pid, _ in gantt_chart:
        print(f" {pid} |", end="")
    print("\n", end="")

    print("0", end="")
    for i in range(len(gantt_chart)):
        if i < len(gantt_chart) - 1:
            next_time = gantt_chart[i + 1][1]
        else:
            next_time = current_time
        print(f"   {next_time}", end="")
    print("\n")

    # Display results table
    print("\n" + "=" * 90)
    print(
        f"{'Process':<10} {'Arrival':<10} {'Burst':<10} {'Priority':<10} {'Completion':<12} {'Turnaround':<12} {'Waiting':<10}")
    print("=" * 90)

    total_waiting = 0
    total_turnaround = 0

    for p in processes:
        print(
            f"{p.pid:<10} {p.arrival:<10} {p.burst:<10} {p.priority:<10} {p.completion:<12} {p.turnaround:<12} {p.waiting:<10}")
        total_waiting += p.waiting
        total_turnaround += p.turnaround

    print("=" * 90)

    # Calculate averages
    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n

    print(f"\n{'Average Waiting Time:':<30} {avg_waiting:.2f} units")
    print(f"{'Average Turnaround Time:':<30} {avg_turnaround:.2f} units")
    print("\n" + "=" * 90)

    return avg_waiting, avg_turnaround


def get_user_processes():
    """Get process details from user input"""
    print("\n" + "=" * 60)
    print("ENTER YOUR OWN PROCESS DETAILS")
    print("=" * 60)

    while True:
        try:
            n = int(input("\nEnter the number of processes: "))
            if n <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    processes = []
    print("\nNote: Higher priority number = Higher priority")
    print("-" * 60)

    for i in range(n):
        print(f"\nProcess {i + 1}:")
        while True:
            try:
                pid = input(f"  Enter Process ID (e.g., P{i + 1}): ").strip()
                if not pid:
                    print("  Process ID cannot be empty.")
                    continue

                arrival = int(input(f"  Enter Arrival Time: "))
                if arrival < 0:
                    print("  Arrival time cannot be negative.")
                    continue

                burst = int(input(f"  Enter Burst Time: "))
                if burst <= 0:
                    print("  Burst time must be positive.")
                    continue

                priority = int(input(f"  Enter Priority: "))

                processes.append(Process(pid, arrival, burst, priority))
                break
            except ValueError:
                print("  Invalid input. Please enter valid numbers.")

    return processes


def run_with_default_data():
    """Run scheduling with the predefined process data"""
    processes = [
        Process("P1", 0, 4, 2),
        Process("P2", 1, 3, 3),
        Process("P3", 2, 1, 4),
        Process("P4", 3, 5, 5),
        Process("P5", 4, 2, 5)
    ]

    print("\nInput Process Details:")
    print("-" * 60)
    print(f"{'Process ID':<12} {'Arrival Time':<15} {'Burst Time':<12} {'Priority':<10}")
    print("-" * 60)
    for p in processes:
        print(f"{p.pid:<12} {p.arrival:<15} {p.burst:<12} {p.priority:<10}")
    print("-" * 60)
    print("\nNote: Higher priority number = Higher priority")

    return processes


# Main program
if __name__ == "__main__":
    # Run with default data first
    print("\n" + "=" * 60)
    print("RUNNING WITH DEFAULT PROCESS DATA")
    print("=" * 60)

    processes = run_with_default_data()
    avg_wt, avg_tat = preemptive_priority_scheduling(processes)
    print("\n✓ Scheduling Complete!")

    # Ask if user wants to try with their own input
    while True:
        print("\n" + "=" * 60)
        choice = input("\nDo you want to try with your own input? (yes/no): ").strip().lower()

        if choice in ['yes', 'y']:
            user_processes = get_user_processes()
            avg_wt, avg_tat = preemptive_priority_scheduling(user_processes)
            print("\n✓ Scheduling Complete!")
        elif choice in ['no', 'n']:
            print("\nThank you for using the Preemptive Priority Scheduler!")
            break
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")
            continue
