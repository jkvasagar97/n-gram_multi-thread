
import sys
import time
from utils.thread_utils import cThread
from utils.file_utils import cFileFolderHandle

def main(pDirPath, pNoThread, pNVal, pKValue):
    
    #Reading files 
    startTime = time.time()
    fileHandler = cFileFolderHandle(pDirPath, pNoThread)
    fileHandler.start_read()
    endTime = time.time()
    print("Time for reading is {}".format(endTime - startTime))
    with open ("temp.txt", "w") as f:
        for key, value in fileHandler.wordsInClass.items():
            f.write('%s:%s\n' % (key, value))

    

if __name__ == "__main__": # entry point
    if len(sys.argv) != 5:
        print("Expected number of arguments not satisfied")
        exit()
    
    filename = sys.argv[1]
    noThread = int(sys.argv[2])
    nVal = int(sys.argv[3])
    kVal = int(sys.argv[4])

    main(filename, noThread, nVal, kVal)
