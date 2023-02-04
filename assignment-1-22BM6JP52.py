import sys
import re
from os import listdir, path


class nGramBatchWise:
    def __init__(self, pSourceFolderPath, pNvalue, pBatch):
        self.folder_path = pSourceFolderPath
        self.n = pNvalue
        self.batch = pBatch
        self.tokens = {}
        self.ngramsClasswise = {}
        self.score = {}

    def read_files(self):
        regex_expression = '[^a-zA-Z0-9]+'
        for cl in self.batch:
            self.tokens[cl] = []
            classPath = path.join(self.folder_path, cl)
            for file in listdir(classPath):
                with open(path.join(classPath, file), encoding="latin-1") as fHandle:
                    self.tokens[cl].append(re.split(regex_expression, fHandle.read().lower()))

    def gen_ngram(self):
        for cl in self.batch:
            self.ngramsClasswise[cl] = []
            for wordsInFile in self.tokens[cl]:
                for i in range(len(wordsInFile)- self.n+1):
                    self.ngramsClasswise[cl].append(" ".join(wordsInFile[i:i+self.n]))
    
    def comp_score(self):
        for cl in self.batch:
            self.score[cl] = {}
            noOfFiles = len(self.tokens[cl])
            for ngram in self.ngramsClasswise[cl]:
                if ngram in self.score[cl]:
                    self.score[cl][ngram] = self.score[cl][ngram] + (1/noOfFiles)
                else:
                    self.score[cl][ngram] =   1/noOfFiles

    def sort_ngrams(self):
        for cl in self.batch:
            self.score[cl] = sorted(self.score[cl].items(), reverse=True, key= lambda x: x[1])

if __name__=="__main__":

    if len(sys.argv) != 5:
            print("Expected number of arguments not satisfied")
            exit()
    
    filename = sys.argv[1]
    noThread = int(sys.argv[2])
    nVal = int(sys.argv[3])
    kVal = int(sys.argv[4])
    print("filename : {}, noThread : {}, nVal : {}, kVal : {}".format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    handel = nGramBatchWise(filename, nVal, listdir(filename))
    handel.read_files()
    handel.gen_ngram()
    handel.comp_score()
    handel.sort_ngrams()
    print(handel.score)