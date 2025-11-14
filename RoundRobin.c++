#include <algorithm>
#include <iostream>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

// structure of each process
struct process {
  int pid;
  int arrival_time;
  int burst_time;
};

// result struct to show results of the algorithm calculation
struct Result {
  unordered_map<int, int> completion;
  unordered_map<int, int> turnaroundtime;
  unordered_map<int, int> waitingtime;
};

// round robin algorithm
Result Roundrobin(const vector<process> &processes, int time_quantum) {
  vector<process> procs = processes;

  // Sort by arrival
  stable_sort(procs.begin(), procs.end(),
              [](auto &a, auto &b) { return a.arrival_time < b.arrival_time; });

  int n = procs.size();
  unordered_map<int, int> rem, arrival, burst;
  for (auto &p : procs) {
    rem[p.pid] = p.burst_time;
    arrival[p.pid] = p.arrival_time;
    burst[p.pid] = p.burst_time;
  }

  queue<int> q;
  vector<tuple<int, int, int>> gantt;
  unordered_map<int, int> completion;

  int time = 0;
  int idx = 0;

  // Main loop
  while (idx < n || !q.empty()) {

    // Admit processes that have arrived
    while (idx < n && procs[idx].arrival_time <= time) {
      q.push(procs[idx].pid);
      idx++;
    }

    if (q.empty()) {
      time = procs[idx].arrival_time; // CPU idle, jump forward
      continue;
    }

    int pid = q.front();
    q.pop();

    int exec = min(time_quantum, rem[pid]);

    gantt.push_back({time, time + exec, pid});
    time += exec;
    rem[pid] -= exec;

    // Admit new arrivals that appeared during execution
    while (idx < n && procs[idx].arrival_time <= time) {
      q.push(procs[idx].pid);
      idx++;
    }

    if (rem[pid] > 0)
      q.push(pid); // Not done, return to queue
    else
      completion[pid] = time; // Finished
  }

  // Build result object
  unordered_map<int, int> tat, wt;
  for (auto &p : procs) {
    int pid = p.pid;
    tat[pid] = completion[pid] - arrival[pid];
    wt[pid] = tat[pid] - burst[pid];
  }

  return {completion, tat, wt};
}

int main() {
  int quantum = 2; // given time quantum
  vector<process> procs = {
      {1, 0, 5}, // P1: arrival 0, burst 5
      {2, 1, 3}, // P2: arrival 1, burst 3
      {3, 2, 1}, // P3: arrival 2, burst 1
      {4, 3, 2}, // P4: arrival 3, burst 2
      {5, 4, 3}  // P5: arrival 4, burst 3
  };
  Result r = Roundrobin(procs, quantum);

  cout << "Process\tCompletion\tTurnaround\tWaiting" << endl;
  int total_waiting = 0;
  for (auto &p : procs) {
    cout << "P" << p.pid << "\t" << r.completion[p.pid] << "\t\t"
         << r.turnaroundtime[p.pid] << "\t\t" << r.waitingtime[p.pid] << endl;
    total_waiting += r.waitingtime[p.pid];
  }
  cout << "\nAverage Waiting Time: " << (double)total_waiting / procs.size()
       << endl;

  return 0;
}
