
import sys
import time
import json
from utils.file_utils import cFileFolderHandle

def main(pDirPath, pNoThread, pNVal, pKValue):
    
    #Reading files 
    startTime = time.time()
    fileHandler = cFileFolderHandle(pDirPath, pNoThread)
    fileHandler.start_read()
    endTime = time.time()

    #------------- Checking output --------------------------------------
    print("Time for reading is {}".format(endTime - startTime))
    print("Number of classes: {}".format(len(fileHandler.wordsInClass)))
    for cl in fileHandler.wordsInClass.keys():
        print("\t - {} : {}".format(cl, len(fileHandler.wordsInClass[cl])))

    with open("temp.json", "w") as temp: # writing words into json file
        json.dump(fileHandler.wordsInClass, temp)
    #---------------------------------------------------------------------

    
    

if __name__ == "__main__": # entry point
    if len(sys.argv) != 5:
        print("Expected number of arguments not satisfied")
        exit()
    
    filename = sys.argv[1]
    noThread = int(sys.argv[2])
    nVal = int(sys.argv[3])
    kVal = int(sys.argv[4])

    main(filename, noThread, nVal, kVal)
