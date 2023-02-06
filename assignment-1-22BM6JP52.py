import sys
import re
from os import listdir, path
import threading
import time

def combine_resuts(pResults):
    """
    Reduce function to combine results from several threads
    """
    combined_result = {}
    for _, ngrams in pResults.items():
        for ngram, score in ngrams.items():
            if ngram not in combined_result.keys():
                combined_result[ngram] = score
            elif combined_result[ngram] < score:
                combined_result[ngram] = score
    return combined_result

class nGramBatchWise:
    """
    Class to genreate scores of n gram batchwise, that can be run using multi threading
    and sort the results in decending order
    """
    def __init__(self, pSourceFolderPath, pNvalue, pBatch):
        self.folder_path = pSourceFolderPath
        self.n = pNvalue
        self.batch = pBatch
        self.tokens = {}
        self.ngramsClasswise = {}
        self.score = {}
        self.no_of_files = {}

    def read_files(self):
        regex_expression = '[^a-zA-Z0-9]+'
        for cl in self.batch:
            self.tokens[cl] = []
            classPath = path.join(self.folder_path, cl)
            files = listdir(classPath)
            self.no_of_files[cl] = len(files)
            for file in files:
                with open(path.join(classPath, file), encoding="latin-1") as fHandle:
                    self.tokens[cl].append(re.split(regex_expression, fHandle.read().lower()))

    def gen_ngram(self):
        for cl in self.batch:
            self.ngramsClasswise[cl] = []
            for wordsInFile in self.tokens[cl]:
                for i in range(len(wordsInFile)- self.n+1):
                    self.ngramsClasswise[cl].append(" ".join(wordsInFile[i:i+self.n]))
        del self.tokens
    
    def comp_score(self):
        for cl in self.batch:
            self.score[cl] = {}
            noOfFiles = self.no_of_files[cl]
            for ngram in self.ngramsClasswise[cl]:
                if ngram in self.score[cl]:
                    self.score[cl][ngram] = self.score[cl][ngram] + (1/noOfFiles)
                else:
                    self.score[cl][ngram] =   1/noOfFiles
        del self.ngramsClasswise

    def sort_ngrams(self):
        for cl in self.batch:
            self.score[cl] = dict(sorted(self.score[cl].items(), reverse=True, key= lambda x: x[1]))

def thread_function(pHandle):
    """
    The function run in multi threading taking the class as arguments
    """
    pHandle.read_files()
    pHandle.gen_ngram()
    pHandle.comp_score()
    pHandle.sort_ngrams()

if __name__=="__main__":

    start  =time.time()

    if len(sys.argv) != 5:
            print("Expected number of arguments not satisfied")
            exit()
    
    filename = sys.argv[1]
    noThread = int(sys.argv[2])
    nVal = int(sys.argv[3])
    kVal = int(sys.argv[4])
    print("filename : {}, noThread : {}, nVal : {}, kVal : {}".format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))

    #Init batches and thread handles
    batches = [[] for _ in range(noThread)]
    batch_handles = []
    thread_handle = []

    #allocating batches 
    for i, cl in enumerate(listdir(filename)):
        batches[i%noThread].append(cl)
    
    #init and starting the thread function 
    for batch in batches:
        batch_handles.append(nGramBatchWise(filename, nVal, batch))
        thread_handle.append(threading.Thread(target= thread_function, args= [batch_handles[-1]]))
        thread_handle[-1].start()

    #waiting fo the threads to join
    for thread in thread_handle:
        thread.join()

    combined_resuts = {}

    #combining the batch wise results 
    for batch_handle in batch_handles:
        combined_resuts = combined_resuts | batch_handle.score

    #reducing the ngrams accoring to the maximum score they got across classes
    combined_resuts = combine_resuts(combined_resuts)

    print("Time taken for everything other than sort {}".format(time.time() - start))

    #sorting wrt scores, to display the top n values
    combined_resuts = sorted(combined_resuts.items(), reverse=True, key= lambda x:x[1])
    print(combined_resuts[:kVal])

    print("Total time taken {}".format(time.time() - start))