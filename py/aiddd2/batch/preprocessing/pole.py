import pandas as pd

import aiddd2.common.config as cfg
from aiddd2.common.log import Log
from aiddd2.batch.data_manager import saveData

def ppPole(df, trainingDf):
    logs = Log('pp pole')
    
    selectColumns = [
        'cons_id', 'comp_id',
        'pole_shape_cd', 'pole_type_cd', 'pole_spec_cd',
        'coordinate'
    ]
    selectDf = df[selectColumns].copy()
    
    # 공사번호가 있는 전주 데이터 추출
    selectDf = selectDf[selectDf.cons_id.isin(trainingDf.cons_id)]
    
    # 'coordinate' 컬럼을 이용해 좌표정보 컬럼 추가
    selectDf[['x', 'y', 'temp1', 'temp2']] = \
        selectDf.coordinate.str.split(',', expand=True)
    selectDf.drop(columns=['temp1', 'temp2', 'coordinate'], inplace=True)
    selectDf.x = selectDf.x.astype(float)
    selectDf.y = selectDf.y.astype(float)
    
    # Code형 데이터 One-Hot Encoding
    selectDf = pd.get_dummies(
        selectDf,
        columns=['pole_shape_cd', 'pole_type_cd', 'pole_spec_cd'],
        prefix=['pole_shape', 'pole_type', 'pole_spec']
    )
    # bool형 타입 데이터를 1과 0으로 변환
    selectDf = selectDf.applymap(lambda x: int(x) if isinstance(x, bool) else x)
    
    logs.mid(
        '공사비 데이터에 전주 데이터(위치, 타입데이터 갯 수 등) 추가 후 형태: '
        f'{selectDf.shape}'
    )