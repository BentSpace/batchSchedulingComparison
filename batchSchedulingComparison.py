from ast import For
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

  # Convert to list of lists
  process = 0
  while process < len(batchFileDataList):
    # Strip out newlines
    batchFileDataList[process] = batchFileDataList[process].strip()
    # Split into list
    batchFileDataList[process] = batchFileDataList[process].split(",")
    process += 1

  # Check Algo name
  algoName = sys.argv[2]
  if (not (algoName == "FCFS" or algoName == "ShortestFirst" or 
    algoName == "Priority")):
      print("\nScheduling algorithm must be FCFS, ShortestFirst or Priority," + 
        " please try again.\n")
      quit()

  # Call the chosen Algo
  if (algoName == "FCFS"):
    FirstComeFirstServedSort(batchFileDataList)
  if (algoName == "ShortestFirst"):
    ShortestJobFirst(batchFileDataList)
  if (algoName == "Priorty"):
    PrioritySort(batchFileDataList)

  
def AverageTurnaround(processCompletionTimes, processArrivalTimes):
  pass

def AverageWait(processTurnaroundTimes, processBurstTime):
  pass

# Returns 
# 1: list of the times each process is completed at
# 2: list containing the PID of the processes in the order the algorithm sorted
def FirstComeFirstServedSort(batchFileData):
  pass

# Returns list of the times each process is completed at
def ShortestJobFirst(batchFileData):
  pass

# Returns list of the times each process is completed at
def PrioritySort(batchFileData):
  pass

if __name__== "__main__":
  main()