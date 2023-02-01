
import sys
import time
import json
from utils.file_utils import cFileFolderHandle
from utils.ngram_utils import CNgram

def main(pDirPath, pNoThread, pNVal, pKValue):
    
    #reading files 
    startTime = time.time()
    fileHandler = cFileFolderHandle(pDirPath, pNoThread)
    fileHandler.start_read()
    endTime = time.time()
    print("Time for reading is {}".format(endTime - startTime))

    #generating ngrams and calculating frequency
    startTime2 = time.time()
    ngram = CNgram( pNoThread, pNVal, fileHandler.wordsInClass)
    ngram.data_to_dict()
    endTime2 = time.time()
    print("Time for generating ngram is {}".format(endTime2 - startTime2))
    #sorting
    startTime3 = time.time()
    sortedClasswise = {}
    for cl in ngram.ngram_freq:
        sortedClasswise[cl] = dict(sorted(ngram.ngram_freq[cl].items(), 
                                key=lambda x:x[1], reverse = True))
    endTime3 = time.time()
    print("Time for sorting is {}".format(endTime3 - startTime3))
    print("Total time: ", endTime3-startTime)
    with open("temp.json", "w") as temp: # writing words into json file
        json.dump(sortedClasswise, temp)

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
