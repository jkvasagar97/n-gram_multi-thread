from .thread_utils import cThread

class CNgram:
    # will take a portion of the overall dict and process the information and find n grams
    def __init__(self, pNoThread, pNval, pData):
        self.ngrams = {}
        self.score = {}
        self.data = pData
        self.nothread = pNoThread
        self.n = pNval
        self.threadHandles = []

    def comp_frequency(self, pBatch):
        for cl in pBatch:
            noOfFiles = len(self.data[cl])
            self.score[cl] = {}
            for fileinclass in self.ngrams[cl]:
                for ngram in fileinclass:
                    if ngram in self.score[cl]:
                        self.score[cl][ngram] = self.score[cl][ngram] + 1/noOfFiles
                    else:
                        self.score[cl][ngram] = 1/noOfFiles

    def gen_ngram(self, pBatch):
        for cl in pBatch:
            self.ngrams[cl] = []
            output = []
            for fileinclass in self.data[cl]:
                for i in range(len(fileinclass)- self.n+1):
                    output.append(" ".join(fileinclass[i:i+self.n]))
            self.ngrams[cl].append(output)

    def combine_results(self):
        self.ngrams = {}
        for cl, ngrams in  self.score.items():
            for ngram, frequency in ngrams.items():
                if ngram not in self.ngrams.keys():
                    self.ngrams[ngram] = frequency
                elif self.ngrams[ngram] < frequency:
                    self.ngrams[ngram] = frequency

    def data_to_dict(self):
        batches = [[] for _ in range(self.nothread)]
        for i, cl in enumerate(self.data):#Defining batches to run thread
            batches[i%self.nothread].append(cl)
        for i, batch in enumerate(batches):#starting each thread
            threadHandle = cThread("Generating {}-gram".format(self.n), i, 
                                   self.gen_ngram, ([batch]))
            threadHandle.start_thread()
            self.threadHandles.append(threadHandle)
        for threadHandle in self.threadHandles: #waiting for threads to join
            threadHandle.wait_thread()

        self.threadHandles = []

        for i, batch in enumerate(batches):#starting each thread
            threadHandle = cThread("Computing frequency {}-gram".format(self.n), i, 
                                   self.comp_frequency, ([batch]))
            threadHandle.start_thread()
            self.threadHandles.append(threadHandle)
        for threadHandle in self.threadHandles: #waiting for threads to join
            threadHandle.wait_thread()
        self.combine_results()