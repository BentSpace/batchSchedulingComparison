# batchSchedulingComparision
# by: Nathan Bertram
# CS 446
# Compares three scheduling algorithms.  First come first served, Shortest Job
# First and Priority.
# Takes two arguements.  First the batch filename you wish to use, with the 
# following information PID, Arrival Time, Burst Time, and Priority seperated by
# commas.  Each process on it's own line.
#
# Compare and Constrast
# In the sample batch file provided, Shortest Job First had the fastest average 
# turnaroud time and shortest average wait time.  So if that is representative
# of normal and if those two traits are most important to you, then that one 
# would be the best.  First come first served certainly is the simpliest to 
# implement and may gain some speed from lesser overhead. Priority would make 
# sense for a system where certain processes are more important to be processed
# sooner than other processes.

import sys
import os
import copy

def main():
  # Path to cwd
  __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
  # Check for 3 args
  if (len(sys.argv) != 3):
    print("\nMust use with 3 arguements. \n" +\
      "File name, batchfile name, and scheduling algorithm. \n" +\
      "Please try again.\n")
    quit()

  batchFileName = sys.argv[1]
  # Check whether file name exists
  file_exists = os.path.exists(batchFileName)
  if (not file_exists):
    print("\nSorry that batch file does not exsist, please try again.\n")
    quit()

  # Open batch file
  batchFile = open(os.path.join(__location__, batchFileName), 'r')
  batchFileDataList = batchFile.readlines()
  batchFileDataListOfDicts = [] 
  arrivalTimes = []
  burstTimes = []
  
  # Check Algo name
  algoName = sys.argv[2]
  if (not (algoName == "FCFS" or algoName == "ShortestFirst" or 
    algoName == "Priority")):
      print("\nScheduling algorithm must be FCFS, ShortestFirst or Priority," + 
        " please try again.\n")
      quit()

  # Convert to list of lists
  i = 0
  while i < len(batchFileDataList):
    process = batchFileDataList[i]
    # Strip out newlines
    process = process.strip()
    # Split into list
    process = process.split(",")
    # Convert all strings to ints
    item = 0
    while item < 4:
      process[item] = int(process[item])
      item += 1
    processDict = {
      "PID": process[0],
      "Arrival Time": process[1],
      "Burst Time": process[2],
      "Priority": process[3] 
    }
    batchFileDataListOfDicts.append(processDict)
    i += 1

  # First sort by PID
  batchFileDataListOfDicts.sort(key=lambda x:x['PID'])
  # Then sort by arrival time
  batchFileDataListOfDicts.sort(key=lambda x:x['Arrival Time'])

  # Call the chosen Algo
  if (algoName == "FCFS"):
    processCompletionTimes, executionOrderList = \
      FirstComeFirstServedSort(batchFileDataListOfDicts)
  if (algoName == "ShortestFirst"):
    processCompletionTimes, executionOrderList = \
      ShortestJobFirst(batchFileDataListOfDicts)
  if (algoName == "Priority"):
    processCompletionTimes, executionOrderList = \
      PrioritySort(batchFileDataListOfDicts)

  # Make list of arrival times
  for process in batchFileDataListOfDicts:
    arrivalTimes.append(process["Arrival Time"])

  # Make list of burst times
  for process in batchFileDataListOfDicts:
    burstTimes.append(process["Burst Time"])

  averageTurnAroundTime, turnAroundTimes = \
    AverageTurnaround(processCompletionTimes, arrivalTimes)

  averageWaitTime = AverageWait(turnAroundTimes, burstTimes)

  print("\nPID ORDER OF EXECUTION\n")
  for PID in executionOrderList:
    print(str(PID) + "\n")
  print("Average Process Turnaround Time: " + str(averageTurnAroundTime))
  print("Average Process Wait Time: " + str(averageWaitTime))

# AverageTurnaround(processCompletionTimes, processArrivalTimes)
# Parameters:
# accepts the time that the process would be completed at by the algorithm, 
# accepts the time that each process arrives
# Returns: 
# (1)the average turn around, 
# (2)a list of each process turn around times
def AverageTurnaround(processCompletionTimes, processArrivalTimes):
  process = 0
  numProcesses = len(processCompletionTimes)
  turnAroundTimes = []
  while process < numProcesses:
    turnAroundTimes.append(processCompletionTimes[process] - 
      processArrivalTimes[process])
    process += 1
  total = 0
  for turnAroundTime in turnAroundTimes:
    total += turnAroundTime
  averageTurnAroundTime = total / numProcesses
  return averageTurnAroundTime, turnAroundTimes

# AverageWait(processTurnaroundTimes, processBurstTime)
# Parameters: 
# accepts the list of process turnaround times that is returned by 
# AverageTurnaround, accepts the burst time of each process
# Returns: 
# (1)AverageWait
def AverageWait(processTurnaroundTimes, processBurstTime):
  process = 0
  numProcesses = len(processTurnaroundTimes)
  waitTimes = []
  while process < numProcesses:
    waitTimes.append(processTurnaroundTimes[process] - 
      processBurstTime[process])
    process += 1
  total = 0
  for waitTime in waitTimes:
    total += waitTime
  averageWaitTime = total / numProcesses
  return averageWaitTime

# FirstComeFirstServedSort(batchFileData)
# Schedules processes by executing the ones with earliest arrival time first
# If two have the same arrival time, process in order of PID
# Parameter:
# a list of processes, each a list containing PID, Arrival Time, 
# Burst Time, and Priority
# Returns:
# 1: list of the times each process is completed at
# 2: list containing the PID of the processes in the order the algorithm sorted
def FirstComeFirstServedSort(batchFileData):
  time = 0
  process = 0
  numProcesses = len(batchFileData)
  processCompletionTimes = []
  PIDsCompletedList = []
  while process < numProcesses:
    currentProcess = batchFileData[process]
    if time < currentProcess["Arrival Time"]:
      time = currentProcess["Arrival Time"]
    time += currentProcess["Burst Time"]
    processCompletionTimes.append(time)
    PIDsCompletedList.append(currentProcess["PID"])
    process += 1
  return processCompletionTimes, PIDsCompletedList


# ShortestJobFirst(batchFileData)
# Parameters: 
# accepts all of the batchFileData from the batchfile opened in main
# Returns: 
# (1) a list  of the time each process is completed at
# (2) a list containing the PID of the processes in the order the algorithm 
# sorted them by.
def ShortestJobFirst(batchFileData):
  time = 0
  processesCompleted = 0
  numProcesses = len(batchFileData)
  notComplete = True
  processQueue = []
  executionOrderList = []
  # Completion Times in new sorted order of batchFileData
  processCompletionTimes = [] 
  while notComplete:
    # If a process's arrival time equals the current time added to the queue
    for process in batchFileData:
      if process["Arrival Time"] == time:
        processCopy = copy.deepcopy(process)
        processQueue.append(processCopy)

    # Sort by remaining time
    processQueue.sort(key=lambda x:x['Burst Time'])

    # If the process of the front of the queue has zero time remaining save 
    # completion time  and pop it off the queue 
    if processQueue[0]["Burst Time"] == 0:
      # Find element in batchFileData matching PID
      PID = processQueue[0]["PID"]
      matchingProcess = next(x for x in batchFileData if x["PID"] == PID)
      matchingProcess["Completion Time"] = time

      processQueue.pop(0)
      processesCompleted += 1

    # If the process at front of queue is not the last executed one then add to 
    # execution list
    if processQueue:
      executingProccessPID = processQueue[0]["PID"]
    if not executionOrderList:
      executionOrderList.append(executingProccessPID)
    elif executionOrderList[-1] != executingProccessPID:
      executionOrderList.append(executingProccessPID)

    # Decrement the process's at the front of the queue's remaining time by one
    if processQueue:
     processQueue[0]["Burst Time"] = processQueue[0]["Burst Time"] - 1
    
    # Check if all process's have completed
    if processesCompleted == numProcesses:
      notComplete = False
    time += 1 
  for process in batchFileData:
    processCompletionTimes.append(process["Completion Time"])
  return processCompletionTimes, executionOrderList

# PrioritySort(batchFileData)
# Parameters: 
# accepts all of the batchFileData from the batchfile opened in main
# Returns: 
# (1)a list of the time each process is completed at, and 
# (2) a list containing the PID of the processes in the order the algorithm 
# sorted them by.
def PrioritySort(batchFileData):
  time = 0
  processesCompleted = 0
  numProcesses = len(batchFileData)
  notComplete = True
  processQueue = []
  tempQueue = []
  executionOrderList = []
  # Completion Times in new sorted order of batchFileData
  processCompletionTimes = [] 

  # At each time
  while notComplete:
    # If a process's arrival time equals the current time added to the queue
    for process in batchFileData:
      if process["Arrival Time"] == time:
        processCopy = copy.deepcopy(process)
        tempQueue.append(processCopy)

    # Sort Temp Queue by PID
    tempQueue.sort(key=lambda x:x['PID'])
    # Sort Temp Queue by Priority
    tempQueue.sort(key=lambda x:x['Priority'])

    # Add tempQueue to actual queue
    while tempQueue:
      processQueue.append(tempQueue.pop(0))


    # If the process of the front of the queue has zero time remaining save 
    # completion time  and pop it off the queue 
    if processQueue[0]["Burst Time"] == 0:
      # Find element in batchFileData matching PID
      PID = processQueue[0]["PID"]
      matchingProcess = next(x for x in batchFileData if x["PID"] == PID)
      matchingProcess["Completion Time"] = time

      processQueue.pop(0)
      processesCompleted += 1

    # If the process at front of queue is not the last executed one then add to 
    # execution list
    if processQueue:
      executingProccessPID = processQueue[0]["PID"]
    if not executionOrderList:
      executionOrderList.append(executingProccessPID)
    elif executionOrderList[-1] != executingProccessPID:
      executionOrderList.append(executingProccessPID)

    # Decrement the process's at the front of the queue's remaining time by one
    if processQueue:
     processQueue[0]["Burst Time"] = processQueue[0]["Burst Time"] - 1
    
    # Check if all process's have completed
    if processesCompleted == numProcesses:
      notComplete = False
    time += 1 
  for process in batchFileData:
    processCompletionTimes.append(process["Completion Time"])
  return processCompletionTimes, executionOrderList



if __name__== "__main__":
  main()