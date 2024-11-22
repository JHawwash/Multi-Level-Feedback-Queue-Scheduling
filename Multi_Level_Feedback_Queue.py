from collections import deque # double ended queue needed for ready queue

# Global Variable for current time
current_time = 0

# Creating a class for Processes
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid # Process ID
        self.arrival_time = arrival_time # Arrival Time
        self.burst_time = burst_time # Burst Time
        self.remaining_time = burst_time # Remaining Time from Burst Time
        self.response_time = -1 # Response Time
        self.wait_time = 0 # Waiting Time
        self.turnaround_time = 0 # Turnaround Time
        self.execution_time = 0 # Execution Time

# Round Robin Scheduling
def roundRobin8(processes):
    quantum = 8
    ready_queue = deque() # Ready Queue for processes (Double Ended Queue, processes can be removed from both ends)
    completed_processes = [] # List of completed processes
    global current_time # Current Time
    
    incomplete_processes = []
    visited = 0
    
    for process in processes:
        ready_queue.append(process)
    
    while True:
        
        if len(ready_queue) == 0:
            current_time += 1
    
        current_process = ready_queue.popleft()
        if current_process.response_time == -1:
            current_process.response_time = current_time - current_process.arrival_time
            
        if current_process.burst_time <= quantum:
            current_time += current_process.remaining_time
            current_process.remaining_time = 0
            completed_processes.append(current_process)
            current_process.turnaround_time = current_time - current_process.arrival_time
            current_process.wait_time = current_process.turnaround_time - current_process.burst_time
            current_process.execution_time = current_time
            visited += 1
        
        if current_process.burst_time > quantum:
            current_time += quantum
            current_process.remaining_time -= quantum
            incomplete_processes.append(current_process) # These will go to the second level queue
            visited +=1
        
        if visited == len(processes):
            break
        
    return completed_processes,incomplete_processes


def roundRobin16(processes): # takes incomplete processes from roundRobin8
    quantum = 16
    ready_queue = deque() # Ready Queue for processes (Double Ended Queue, processes can be removed from both ends)
    completed_processes = [] # List of completed processes
    global current_time  # Current Time
    
    incomplete_processes = []
    
    visited = 0
    
    for process in processes:
        ready_queue.append(process)
    
    while True:
        
        if len(ready_queue) == 0:
            current_time += 1
    
        current_process = ready_queue.popleft()
        if current_process.response_time == -1:
            current_process.response_time = current_time - current_process.arrival_time
            
        if current_process.remaining_time <= quantum:
            current_time += current_process.remaining_time
            current_process.remaining_time = 0
            completed_processes.append(current_process)
            current_process.turnaround_time = current_time - current_process.arrival_time
            current_process.wait_time = current_process.turnaround_time - current_process.remaining_time
            current_process.execution_time = current_time
            visited += 1
        
        if current_process.burst_time > quantum:
            current_time += quantum
            current_process.remaining_time -= quantum
            incomplete_processes.append(current_process) # These will go to the second level queue
            visited +=1
        
        if visited == len(processes):
            break
        
    return completed_processes,incomplete_processes     
        



# First-Come-First-Serve Scheduling
def FCFS(processes):
    completed_processes = [] # List of completed processes
    
    global current_time # Current Time
    
    for process in processes:
        if process.response_time == -1: # If response time is not set (-1 is default value)
            process.response_time = current_time - process.arrival_time # Set response time
            
        current_time += process.remaining_time # Add burst time to current time
        process.execution_time = current_time # Set process finish time
        process.turnaround_time = process.execution_time - process.arrival_time # calculate and set process turnaround time
        process.wait_time = process.turnaround_time - process.remaining_time # calculate and set process waiting time
        completed_processes.append(process) # Add process to completed processes
    return completed_processes



def performance(processes):
    
    average_waiting_time = 0
    average_response_time = 0
    average_turnaround_time = 0
    global current_time
    
    for i in processes:
        average_waiting_time += i.wait_time
        average_response_time += i.response_time
        average_turnaround_time += i.turnaround_time
        
    average_waiting_time /= len(processes)
    average_response_time /= len(processes)
    average_turnaround_time /= len(processes)
    print("\n-Overall Performance of Multi-Level Queue Scheduling-")
    
    print(f"Average Waiting Time: {average_waiting_time:.2f} ms")
    print(f"Average Response Time: {average_response_time:.2f} ms")
    print(f"Average Turnaround Time: {average_turnaround_time:.2f} ms")
    print(f"\nAll Processes Finished Executing in {current_time} ms\n")
    
    
    for p in processes:
        print(f"-----Process {p.pid}-----")
        print(f"Execution Time: {p.execution_time} ms")
        print(f"Waiting Time: {p.wait_time} ms")
        print(f"Response Time: {p.response_time} ms")
        print(f"Turnaround Time: {p.turnaround_time} ms\n")
    







# Main Program
def main():

    n = int(input("Enter Number of Processes: "))
    arrival_time = input("Enter Arrival Times (Separated by a Space): ").split(' ')
        
    burst_time = input("Enter Burst Times (Separated by a Space): ").split(' ')
        
    # Changing list items from string to int
    arrival_time = [eval(i) for i in arrival_time]
    burst_time = [eval(i) for i in burst_time]
        
    processes = []
        
    for p in range(n):
        process = Process((p+1), arrival_time[p], burst_time[p])
        processes.append(process)
        
         

    completedProcesses1,incompleteProcesses1 = roundRobin8(processes)
    orderOfExecution = []
    print("--------------------Report--------------------")
    
    
    print("Proccesses that Finished while in Queue 1: [", end = " ")
    for p in completedProcesses1:
        print(p.pid, end =" ")
        orderOfExecution.append(p.pid)
    print("]")
    if len(completedProcesses1) < n:
        completedProcesses2,incompleteProcesses2 = roundRobin16(incompleteProcesses1)
        
        if len(completedProcesses2) > 0:
            print("Proccesses that Finished while in Queue 2: [", end = " ")
            for p in completedProcesses2:
                print(p.pid, end =" ")
                orderOfExecution.append(p.pid)
            print("]")
            if len(completedProcesses1) + len(completedProcesses2) < n:
                completeprocesses3 = FCFS(incompleteProcesses2)
                
                if len(completeprocesses3) > 0:
                    print("Proccesses that Finished while in Queue 3: [", end = " ")
                    for p in completeprocesses3:
                        print(p.pid, end =" ")
                        orderOfExecution.append(p.pid)
                    print("]")
    
    print("\nOrder in which processes are executed:", end = " ")
    print(orderOfExecution)
    
    
    
    
    for p in processes:
        print(f"Process {p.pid} Execution Time: {p.execution_time} ms")
        
    
    performance(processes)


    
    
    # cpu_time = [60, 25, 15]
    # current_time = 0
    # total_cpu_time = sum(burst_time)
   


if __name__ == "__main__":
    main()

    exit = input("Press Enter to Exit")