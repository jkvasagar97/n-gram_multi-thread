
import sys
import time
import json
import math
from utils.file_utils import cFileFolderHandle
from utils.ngram_utils import CNgram
from utils.thread_utils import cThread

def sort_batches(pNgramFreq, pBatch, result):
    print(result)
    for cl in pBatch:
        temp = sorted(pNgramFreq[cl].items(), key=lambda x:x[1], reverse = True)
        result = result + temp
        print(temp)
        

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
    batches = [[] for _ in range(pNoThread)]
    threadHandles = []
    result = []
    for index, cl in enumerate(ngram.ngram_freq):
        batches[index%pNoThread].append(cl)
    for i, batch in enumerate(batches):#starting each thread
            threadHandle = cThread("Sorting", i, 
                                   sort_batches, (ngram.ngram_freq, batch, result))
            threadHandle.start_thread()
            threadHandles.append(threadHandle)
    for threadHandle in threadHandles: #waiting for threads to join
            threadHandle.wait_thread()
    endTime3 = time.time()
    print(result[0])
    sorted_result = sorted(result, key= lambda x: x[1], reverse=True)
    print("Time for sorting is {}".format(endTime3 - startTime3))
    print("Total time: ", endTime3-startTime)
    print(sorted_result[0])


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
