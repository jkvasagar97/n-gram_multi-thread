import threading
import time

class cThread:
    """
    Class around thread primarly for loging
    """
    def __init__(self, pName, pIndex, pFunctionPointer, pArgv):
        self.thread = threading.Thread(target= pFunctionPointer, args= pArgv)
        self.threadIndex = pIndex
        self.threadName = pName
    
    def start_thread(self):
        print("\t{} thread {} started at {}".format(self.threadName, self.threadIndex, time.ctime(time.time())))
        self.thread.start()

    def wait_thread(self):
        self.thread.join()
        print("\t{} thread {} ended at {}".format(self.threadName, self.threadIndex, time.ctime(time.time())))