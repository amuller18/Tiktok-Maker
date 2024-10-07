import time

class log:
    def __init__(self, logLevel):
        self.logLevel = logLevel
        pass

    def log(self, log):
        if self.logLevel == 0:
            print(log)

    def start(self, process):
        self.time = time.time()
        self.log(process + ' has started...')
    
    def end(self, proccess):
        self.log(proccess + ' has completed in ' + str(round(time.time() - self.time, 3)) + ' seconds...')

