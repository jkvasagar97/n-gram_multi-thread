
import sys
from threads import cThread

def main(pFilename, pNoThread):
    thread_handle = [] * pNoThread
    results = [] * pNoThread
    # TODO: Init thread with function and cummilate result

if __name__ == "__main__": # entry point

    if len(sys.argv) != 3:
        print("Expected number of arguments not satisfied")
        exit()
    
    filename = sys.argv[1]
    noThread = int(sys.argv[2])
    main(filename, noThread)