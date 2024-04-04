import re

import aiddd2.common.config as cfg
from aiddd2.common.log import Log
from aiddd2.batch.data_manager import saveData

def ppCons(df):
    logs = Log('pp cons1')
    
    # 결측치 처리
    df.fillna(0, inplace=True)
    
    # 학습대상 레코드 추출
    trainingConditions = \
        (df.acc_type_name == cfg.COND_ACC_TYPE_NAME) & \
        (df.cont_cap < cfg.COND_MAX_CONT_CAP) & \
        (df.cons_type_cd == cfg.COND_CONS_TYPE_CD) & \
        (df.total_cons_cost < cfg.COND_MAX_TOTAL_CONS_COST)
    df = df[trainingConditions].reset_index(drop=True)
    
    # 일자정보 전처리
    # - '최종변경일시'를 이용해 다양한 일자정보 컬럼 추가
    df['year'] = df.last_mod_date.dt.year
    df['month'] = df.last_mod_date.dt.month 
    df['day'] = df.last_mod_date.dt.day
    df['dayofweek'] = df.last_mod_date.dt.dayofweek
    df['dayofyear'] = df.last_mod_date.dt.dayofyear
    df['year_month'] = df.last_mod_date.dt.strftime('%Y%m').astype(int)
    
    # 사번 전처리
    # '최종변경자사번'만 사용(모든 데이터가 최초등록자와 최종변경자사번이 동일했음)
    
    # - 사번앞에 있는 영문자를 추출해 새로운 컬럼 추가(영문자가 없으면 'AAA'추가)
    df['eid_code'] = \
        df.last_mod_eid.str.extract('([a-zA-Z]+)', expand=False)
    df.eid_code.fillna('AAA', inplace=True)
    # - 사번 영문자를 학습에 사용하기 위해 숫자로 변경(일련번호)
    df['eid_code_number'] = df.eid_code.rank(method='dense').astype(int)
    # - 사번에서 숫자만 추출해 별도 보관
    df['eid_number'] = \
        df.last_mod_eid.apply(
            lambda x: re.findall(r'\d+', x)[0]
        ).astype(int)
    
    # 사업소명 전처리
    # - 한글 사업소명을 숫자로 변경(일련번호)    
    df['office_number'] = df.office_name.rank(method='dense').astype(int)
    
    # 학습에 필요한 컬럼 추출
    trainingColumns = [
        'cons_id', 'total_cons_cost', 'last_mod_date', 'last_mod_eid',
        'office_name', 'eid_code', # 여기까지는 눈으로 확인하는 데이터
        'cont_cap', 
        'year', 'month', 'day', 'dayofweek', 'dayofyear', 'year_month',
        'eid_code_number', 'eid_number', 'office_number'
    ]
    trainingDf = df[trainingColumns]
    logs.mid(f'학습용 공사비 데이터 1차 전처리 결과: {trainingDf.shape}')
    
    # 전처리 데이터 저장
    saveData(trainingDf, 'cons', 'pp-filename')
    if cfg.SAVE_INTERMEDIATE_FILE:
        saveData(df, 'cons', 'pp-filename-temp')
        
    logs.stop()
    return trainingDf 