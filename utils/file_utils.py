from .thread_utils import cThread
from os import listdir, path


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
                    for line in fHandle:
                        for word in line.split():
                            self.wordsInClass[cl].append(word)
                    
        

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
