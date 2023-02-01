
import sys
import time
import json
from utils.file_utils import cFileFolderHandle
from utils.ngram_utils import CNgram

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
    #---------------------------------------------------------------------

    start_time2 = time.time()
    ngram = CNgram( pNoThread, pNVal, fileHandler.wordsInClass)
    ngram.data_to_dict()
    endTime2 = time.time()
    print("Time for generating ngram is {}".format(endTime2 - start_time2))

    start_time3 = time.time()
    endTime3 = time.time()
    print("Time for flattening json is {}".format(endTime2 - start_time2))

    for x in ngram.ngram_freq[:pKValue]:
        print(x)

    print("Time for soting is {}".format(endTime3 - start_time3))
    with open("temp.json", "w") as temp: # writing words into json file
        json.dump(ngram.ngram_freq, temp)

if __name__ == "__main__": # entry point
    if len(sys.argv) != 5:
        print("Expected number of arguments not satisfied")
        exit()
    
    filename = sys.argv[1]
    noThread = int(sys.argv[2])
    nVal = int(sys.argv[3])
    kVal = int(sys.argv[4])
    print("filename : {}, noThread : {}, nVal : {}, kVal : {}".format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    main(filename, noThread, nVal, kVal)
