
import sys
import time
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
    ngram = CNgram(pNoThread, pNVal, fileHandler.wordsInClass)
    ngram.data_to_dict()
    endTime2 = time.time()
    print("Time for generating ngram is {}".format(endTime2 - startTime2))
    
    #sorting
    result = sorted(ngram.ngrams.items(), reverse=True, key= lambda x: x[1])
    
    print(result[:pKValue])
    print("Total time:", time.time()-startTime)


def get_max(pList):
    max = 0
    index = -1
    for i, item in enumerate (pList):
        if max < item[1]:
            index = i
            max = item[1]
    return index

def get_top_k(pCombinedResult, pK):
    result = []
    temp = []
    while len(result) <= pK:
        temp = [list(value.items())[0] for key, value in pCombinedResult.items()]
        get_max(temp)
    return result
    
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
