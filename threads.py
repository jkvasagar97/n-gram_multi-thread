import threading
import time

class cThread:
    def __init__(self, pIndex ,pFunctionPointer, pArgv):
        self.thread = threading.Thread(target= pFunctionPointer, args= pArgv)
        self.threadIndex = pIndex
    
    def start_thread(self):
        print("Thread {} started at {}".format(self.threadIndex, time.ctime(time.time())))
        self.thread.start()

    def wait_thread(self):
        self.thread.join()
        print("Thread {} ended at {}".format(self.threadIndex, time.ctime(time.time())))