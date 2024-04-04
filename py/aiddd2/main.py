from aiddd2.common.init import AppInit
from aiddd2.common.log import Log

from aiddd2.batch.process import BatchProcess

def main():
    logs = Log ('modeling')

    AppInit()
    BatchProcess()

    logs.stop()

    
if __name__ == '__main__':
    main()