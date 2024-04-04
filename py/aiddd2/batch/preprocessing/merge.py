import pandas as pd

import aiddd2.common.config as cfg
from aiddd2.common.log import Log
from aiddd2.batch.data_manager import saveData

def ppComputeFacilitiesCount(provideData, trainingDf):
    logs = Log('pp compute facilities count')
    
    for dataType in cfg.DATA_TYPE[1:]:
        df = provideData[dataType]
        fcConsId = df.cons_id.value_counts()
        columnName = f'{dataType}_cnt'
        trainingDf = pd.merge(
            trainingDf, fcConsId.rename(columnName),
            left_on='cons_id', right_on=fcConsId.index, how='left'
        )
        # 해당 공사번호에 없는 설비의 경우 'NaN'값으로 설정, 0으로 처리
        trainingDf[columnName].fillna(0, inplace=True)
        
    trainingDataConditions = \
        (trainingDf.pole_cnt >= cfg.COND_MIN_POLE_COUNT) & \
        (trainingDf.pole_cnt <= cfg.COND_MAX_POLE_COUNT) & \
        (trainingDf.line_cnt >= cfg.COND_MIN_LINE_COUNT) & \
        (trainingDf.line_cnt <= cfg.COND_MAX_LINE_COUNT)
        
    conditionsDf = trainingDf[trainingDataConditions]
    logs.mid(f'공사비별 설비 갯 수 계산 후 데이터 크기: {conditionsDf.shape}')
    
    # 전처리 데이터 저장
    saveData(conditionsDf, 'count', 'pp-filename')
    if cfg.SAVE_INTERMEDIATE_FILE:
        saveData(trainingDf, 'count', 'pp-filename-temp')
        
    logs.stop()
    return conditionsDf
    