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
        self.wordsInClass = []
        self.subDirs = None
        self.fileHandles = None

    def treverse_classes(self, pClassesBatch):
        """
        Reads each file into file handle, which can be used to find n grams
        """
        for cl in pClassesBatch: #Get list of all words in a class
            classPath = path.join(self.dirPath, cl)
            files = listdir(classPath)
            for file in files:
                with open(path.join(classPath, file), encoding="latin-1") as fHandle:
                    for line in fHandle:
                        for word in line.split():
                            self.wordsInClass.append(word)
                    
        

    def start_read(self):
        """
        Reads the all the files in all sub folders into file handles 
        Uses multiple threads
        """
        self.subDirs = listdir(self.dirPath)
        threadLoad = int(len(self.subDirs) / self.noThread)

        for i in range(0, self.noThread): #starting each thread
            threadHandle = cThread("File treversing", i, 
                                   self.treverse_classes, [self.subDirs[i:i+threadLoad]])
            threadHandle.start_thread()
            self.threadHandles.append(threadHandle)

        for threadHandle in self.threadHandles: #waiting for threads to join
            threadHandle.wait_thread()
