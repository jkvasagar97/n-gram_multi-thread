from .thread_utils import cThread
from os import listdir, path
import re

regex_expression = '[^a-zA-Z0-9]+'

class cFileFolderHandle:
    """
    Handling file/foler related utils
    """
    def __init__(self, pDirPath, pNoThread):
        self.dirPath = pDirPath
        self.noThread = pNoThread
        self.threadHandles = []
        self.wordsInClass = {}
        self.subDirs = None
        self.fileHandles = None

    def to_lower(self,pWords):
        return list(map(lambda x: x.lower(), pWords))

    def treverse_classes(self, pClassesBatch):
        """
        Reads each file into file handle, which can be used to find n grams
        """
        for cl in pClassesBatch: #Get list of all words in a class
            self.wordsInClass[cl] = []
            classPath = path.join(self.dirPath, cl)
            files = listdir(classPath)
            for file in files:
                with open(path.join(classPath, file), encoding="latin-1") as fHandle:
                    words = re.split(regex_expression, fHandle.read())
                    self.wordsInClass[cl].append(self.to_lower(words))
        

    def start_read(self):
        """
        Reads the all the files in all sub folders into file handles 
        Uses multiple threads
        """
        self.subDirs = listdir(self.dirPath)
        batches = [[] for i in range(self.noThread)]

        for i, dirName in enumerate(self.subDirs):#Defining batches to run in each thread
            batches[i%self.noThread].append(dirName)

        for i, batch in enumerate(batches):#starting each thread
            threadHandle = cThread("File treversing", i, 
                                   self.treverse_classes, ([batch]))
            threadHandle.start_thread()
            self.threadHandles.append(threadHandle)

        for threadHandle in self.threadHandles: #waiting for threads to join
            threadHandle.wait_thread()
