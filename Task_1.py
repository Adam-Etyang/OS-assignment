"""
Task 1: First Come First Serve (FCFS) Scheduling Algorithm

FCFS is a non-preemptive scheduling algorithm where the process that arrives 
first in the ready queue is assigned the CPU first. It uses a FIFO queue.

The program calculates:
- Waiting time for each process
- Turnaround time for each process
- Average waiting time for all processes
"""


class Process:
    """Class to represent a process"""

    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def fcfs_scheduling(processes):
    """
    Implement FCFS scheduling algorithm

    Args:
        processes: List of Process objects

    Returns:
        List of processes with calculated metrics
    """
    # Sort processes by arrival time (FCFS principle)
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0

    for process in processes:
        # If CPU is idle, jump to next process arrival time
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        # Calculate completion time
        process.completion_time = current_time + process.burst_time

        # Calculate turnaround time = Completion Time - Arrival Time
        process.turnaround_time = process.completion_time - process.arrival_time

        # Calculate waiting time = Turnaround Time - Burst Time
        process.waiting_time = process.turnaround_time - process.burst_time

        # Update current time
        current_time = process.completion_time

    return processes


def calculate_average_waiting_time(processes):
    """Calculate the average waiting time"""
    total_waiting_time = sum(p.waiting_time for p in processes)
    return total_waiting_time / len(processes)


def display_results(processes):
    """Display the scheduling results in a formatted table"""
    print("\n" + "="*80)
    print("FCFS Scheduling Results")
    print("="*80)

    # Header
    print(f"{'Process ID':<12} {'Arrival':<10} {'Burst':<10} {'Completion':<12} {'Turnaround':<12} {'Waiting':<10}")
    print(f"{'ID':<12} {'Time (ms)':<10} {'Time (ms)':<10} {'Time (ms)':<12} {'Time (ms)':<12} {'Time (ms)':<10}")
    print("-"*80)

    # Process details
    for process in processes:
        print(f"{process.process_id:<12} {process.arrival_time:<10} {process.burst_time:<10} "
              f"{process.completion_time:<12} {process.turnaround_time:<12} {process.waiting_time:<10}")

    print("="*80)

    # Average waiting time
    avg_waiting_time = calculate_average_waiting_time(processes)
    print(f"\nAverage Waiting Time: {avg_waiting_time:.2f} ms")
    print("="*80)


def main():
    """Main function to run the FCFS scheduling algorithm"""

    # Example from the assignment
    # Process ID | Arrival Time (ms) | Burst Time (ms)
    # P1         | 0                 | 8
    # P2         | 1                 | 4
    # P3         | 2                 | 9
    # P4         | 3                 | 5

    processes = [
        Process("P1", 0, 8),
        Process("P2", 1, 4),
        Process("P3", 2, 9),
        Process("P4", 3, 5)
    ]

    print("\nInput Processes:")
    print(f"{'Process ID':<12} {'Arrival Time (ms)':<20} {'Burst Time (ms)':<15}")
    print("-"*50)
    for p in processes:
        print(f"{p.process_id:<12} {p.arrival_time:<20} {p.burst_time:<15}")

    # Apply FCFS scheduling
    scheduled_processes = fcfs_scheduling(processes)

    # Display results
    display_results(scheduled_processes)

    # Optional: Allow user to input custom processes
    print("\n" + "="*80)
    user_input = input(
        "\nWould you like to test with custom processes? (yes/no): ").strip().lower()

    if user_input == 'yes' or user_input == 'y':
        custom_processes = []
        num_processes = int(input("Enter the number of processes: "))

        for i in range(num_processes):
            print(f"\nProcess {i+1}:")
            pid = input("  Process ID: ").strip()
            arrival = int(input("  Arrival Time (ms): "))
            burst = int(input("  Burst Time (ms): "))
            custom_processes.append(Process(pid, arrival, burst))

        print("\n" + "="*80)
        print("Custom Process Scheduling")

        # Apply FCFS scheduling
        scheduled_custom = fcfs_scheduling(custom_processes)

        # Display results
        display_results(scheduled_custom)


if __name__ == "__main__":
    main()
