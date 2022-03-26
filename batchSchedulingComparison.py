import sys

def main():
  print("Hello World!")
  print('Number of arguments:', len(sys.argv), 'arguments.')
  print('Argument List:', str(sys.argv))
  if (len(sys.argv) != 3):
    print("\nMust use with 3 arguements. \n" +\
    "File name, batchfile name, and scheduling algorithm. \n" +\
    "Please try again.\n")
    quit()
if __name__== "__main__":
  main()

# print("Guru99")
