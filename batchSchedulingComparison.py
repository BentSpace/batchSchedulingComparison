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

  # Check Algo name
  algoName = sys.argv[2]
  if (not (algoName == "FCFS" or algoName == "ShortestFirst" or 
    algoName == "Priority")):
      print("\nScheduling algorithm must be FCFS, ShortestFirst or Priority," + 
        " please try again.\n")
      quit()
  
if __name__== "__main__":
  main()