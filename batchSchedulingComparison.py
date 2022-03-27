from ast import For
from concurrent.futures import process
import sys
import os

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

  # Call the chosen Algo
  if (algoName == "FCFS"):
    processCompletionTimes, PIDsCompletedList = \
      FirstComeFirstServedSort(batchFileDataListOfDicts)
  if (algoName == "ShortestFirst"):
    ShortestJobFirst(batchFileDataList)
  if (algoName == "Priorty"):
    PrioritySort(batchFileDataList)

  # Make list of arrival times
  # for process in 

  print("\nPID ORDER OF EXECUTION\n")
  for PID in PIDsCompletedList:
    print(str(PID) + "\n")

# AverageTurnaround(processCompletionTimes, processArrivalTimes)
# Parameters:
# accepts the time that the process would be completed at by the algorithm, 
# accepts the time that each process arrives
# Returns: 
# (1)the average turn around, 
# (2)a list of each process turn around times
def AverageTurnaround(processCompletionTimes, processArrivalTimes):
  pass

def AverageWait(processTurnaroundTimes, processBurstTime):
  pass

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
  # First sort by PID
  batchFileData = sorted(batchFileData, key=lambda x:x['PID'])
  # Then sort by arrival time
  batchFileData = sorted(batchFileData, key=lambda x:x['Arrival Time'])
  # Now is order of execution
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

# Returns list of the times each process is completed at
def ShortestJobFirst(batchFileData):
  pass

# Returns list of the times each process is completed at
def PrioritySort(batchFileData):
  pass

if __name__== "__main__":
  main()