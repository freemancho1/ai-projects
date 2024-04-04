from aiddd2.batch.data_manager import getProvideData
from aiddd2.batch.preprocessing.cons import ppCons
from aiddd2.batch.preprocessing.merge import ppComputeFacilitiesCount

class BatchProcess:
    def __init__(self):
        self.provideData = None
        self.trainingDf = None
        self._start()
        
    def _start(self):
        self._loadData()
        self._preprocessing()
        
    def _loadData(self):
        self.provideData = getProvideData() 
        
    def _preprocessing(self):
        self.trainingDf = ppCons(self.provideData['cons'])
        self.trainingDf = ppComputeFacilitiesCount(
            self.provideData, self.trainingDf
        )
        