import os
import pandas as pd
from datetime import datetime

import aiddd2.common.config as cfg
import aiddd2.common.message as msg
from aiddd2.common.log import Log


def getPath(dataType='cons', fileType='filename'):
    pathList = [
        cfg.BASE_DATA_PATH,
        cfg.DATA_INFO[dataType][fileType]
    ]
    return os.path.join(*pathList)

def readData(dataType='cons', fileType='filename', **kwargs):
    filePath = getPath(dataType, fileType)
    _, fileExt = os.path.splitext(filePath)
    
    if fileExt.lower() == '.xlsx':
        return pd.read_excel(filePath, **kwargs)
    if fileExt.lower() == '.csv':
        return pd.read_csv(filePath, **kwargs)
    
    raise ValueError(
        f'{msg.ERROR["fileExt"]}: {filePath}, '
        f'{msg.SOLUTION["fileExt"]}'
    )
    
def saveData(df, dataType, fileType, **kwargs):
    filePath = getPath(dataType, fileType)
    if 'index' not in kwargs:
        kwargs['index'] = False
    df.to_csv(filePath, **kwargs)
    
def getRenameColumns(columns):
    return {
        name: cfg.COMMON_COLUMNS[name]
        for name in cfg.COMMON_COLUMNS if name in columns
    }
    
def getProvideData():
    logs = Log('get provide data')
    provideData = {}
    for dataInfo in cfg.DATA_TYPE:
        startTime = datetime.now()
        df = readData(dataInfo, 'filename')
        # 학습에 사용할 컬럼을 영문으로 변환
        df.rename(columns=getRenameColumns(df.columns), inplace=True)
        provideData[dataInfo] = df
        logs.mid(
            f'읽은 데이터: {dataInfo}, 데이터 크기: {df.shape}, '
            f'처리 시간: {datetime.now()-startTime}'
        )
    logs.stop()
    return provideData