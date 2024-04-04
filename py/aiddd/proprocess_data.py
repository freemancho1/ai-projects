import re
import pandas as pd

import aiddd.app.config as CFG
from aiddd.utils.logs import Log
from aiddd.utils.data_manager import write_data, get_rename_columns

def preprocess(provide_data): 
    logs_preprocess = Log()
    logs_preprocess.start('전처리 작업 시작...') 
    
    df_training = _preprocess_cons(provide_data['cons'], 'cons')
    df_training = _compute_facilities_count(provide_data, df_training)
    df_training = _preprocess_pole(provide_data['pole'], 'pole', df_training)
    df_training = _preprocess_line(provide_data['line'], 'line', )
    
    logs_preprocess.stop('전처리 작업 종료...')
    
'''
공사비데이터를 읽고, 데이터를 전처리한 후 필요한 컬럼만 추출해 파일로 저장
'''
def _preprocess_cons(df_cons, dtype):
    logs_cons = Log()
    logs_cons.start('공사비 전처리 작업 시작...')
    
    # 결측치 처리
    df_cons.fillna(0, inplace=True)
    
    # 학습대상 레코드 추출
    training_data_conditions = \
        (df_cons.acc_type_name == CFG.COND_ACC_TYPE_NAME) & \
        (df_cons.cont_cap < CFG.COND_MAX_CONT_CAP) & \
        (df_cons.cons_type_cd == CFG.COND_CONS_TYPE_CD) & \
        (df_cons.total_cons_cost < CFG.COND_MAX_TOTAL_CONS_COST)
    df_cons = df_cons[training_data_conditions].reset_index(drop=True)
    
    # 일자정보 전처리
    # - '최종변경일시'를 사용해 다양한 일자정보 추가
    df_cons['year'] = df_cons.last_mod_date.dt.year
    df_cons['month'] = df_cons.last_mod_date.dt.month
    df_cons['day'] = df_cons.last_mod_date.dt.day
    df_cons['dayofweek'] = df_cons.last_mod_date.dt.dayofweek
    df_cons['dayofyear'] = df_cons.last_mod_date.dt.dayofyear
    df_cons['year_month'] = df_cons.last_mod_date.dt.strftime('%Y%m').astype(int)

    # 사번 전처리
    # '최종변경자사번'만 사용(모든 데이터가 최초등록자와 최종변경자사번이 동일했음)
    # - 사번앞에 있는 영문자를 추출해 새로운 컬럼 추가(영문자가 없으면 'AAA'추가)
    df_cons['eid_code'] = \
        df_cons.last_mod_eid.str.extract('([a-zA-Z]+)', expand=False)
    df_cons.eid_code.fillna('AAA', inplace=True)
    # - 사번 영문자를 학습에 사용하기 위해 숫자로 변경
    df_cons['eid_code_number'] = \
        df_cons.eid_code.rank(method='dense').astype(int)
    # - 사번에서 숫자만 추출해 별도 보관
    df_cons['eid_number'] = \
        df_cons.last_mod_eid.apply(lambda x: re.findall(r'\d+', x)[0]).astype(int)

    # 사업소명 전처리: 한글 사업소명을 숫자로 변경
    df_cons['office_number'] = \
        df_cons.office_name.rank(method='dense').astype(int)
    
    # 학습에 필요한 컬럼 추출
    training_columns = [
        'cons_id', 'total_cons_cost', 'last_mod_date', 'last_mod_eid',
        'office_name', 'eid_code', # 여기까지는 눈으로 확인하는 데이터
        'cont_cap', 
        'year', 'month', 'day', 'dayofweek', 'dayofyear', 'year_month',
        'eid_code_number', 'eid_number', 'office_number'
    ]
    df_cons_training = df_cons[training_columns]
    logs_cons.mid(f'학습용 공사비 데이터 형태: {df_cons_training.shape}')
    
    # 전처리 데이터 저장
    write_data(CFG.PREPROCESS_DATA_INFO[dtype]['filename'], df_cons_training)
    if CFG.SAVE_INTERMEDIATE_FILE:
        write_data(CFG.PREPROCESS_DATA_INFO[dtype]['filename_all'], df_cons)
    
    logs_cons.stop('공사비 전처리 작업 종료...')
    return df_cons_training
    
'''
전처리된 공사비를 기준으로 전주/전선/인입선의 갯 수를 계산해 파일로 저장
'''
def _compute_facilities_count(provide_data, df_training):
    logs_compute = Log()
    logs_compute.start('공사번호별 설비(전주/전선/인입선) 갯 수 계산 시작...')
    
    for dtype in CFG.PROVIDE_DATA[1:]:
        df_curr = provide_data[dtype]
        facility_count_per_cons_id = df_curr.cons_id.value_counts()
        column_name = f'{dtype}_cnt'
        df_training = pd.merge(
            df_training, facility_count_per_cons_id.rename(column_name),
            left_on='cons_id', right_on=facility_count_per_cons_id.index,
            how='left'
        )
        # 공사비에만 공사번호가 있는 경우 해당 설비값이 NaN으로 들어가기 때문에
        # 0으로 결측치 처리
        df_training[column_name].fillna(0, inplace=True)
        
    training_data_conditions = \
        (df_training.pole_cnt >= CFG.COND_MIN_POLE_COUNT) & \
        (df_training.pole_cnt <= CFG.COND_MAX_POLE_COUNT) & \
        (df_training.line_cnt >= CFG.COND_MIN_LINE_COUNT) & \
        (df_training.line_cnt <= CFG.COND_MIN_LINE_COUNT)
        
    df_training_counts = df_training[training_data_conditions]
    logs_compute.mid(
        f'설비 갯 수가 계산된 학습용 데이터 형태: {df_training_counts.shape}'
    )
    
    # 전처리 데이터 저장
    write_data(
        CFG.PREPROCESS_DATA_INFO['count']['filename'],
        df_training_counts
    )
    if CFG.SAVE_INTERMEDIATE_FILE:
        write_data(
            CFG.PREPROCESS_DATA_INFO['count']['filename_all'],
            df_training
        )
        
    logs_compute.stop('공사번호별 설비(전주/전선/인입선) 갯 수 계산 종료...')
    return df_training_counts
        
def _preprocess_pole(df_pole, dtype, df_training):
    logs_pole = Log()
    logs_pole.start('전주 전처리 작업 시작...')
    
    # 학습에 필요한 컬럼 추출
    training_columns = [
        'cons_id', 'comp_id', 
        'pole_shape_cd', 'pole_type_cd', 'pole_spec_cd',
        'coordinate'
    ]
    df_pole_training = df_pole[training_columns].copy()
    
    # 학습에 필요한 레코드 추출
    # - 전처리된 공사비 데이터에 있는 공사번호만 전주 데이터에서 추출
    df_pole_training = \
        df_pole_training[df_pole_training.cons_id.isin(df_training.cons_id)]
    
    # 'coordinate' 컬럼을 이용해 좌표정보 컬럼 추가
    df_pole_training[['x', 'y', 'temp1', 'temp2']] = \
        df_pole_training.coordinate.str.split(',', expand=True)
    df_pole_training.drop(columns=['temp1', 'temp2', 'coordinate'], inplace=True)
    df_pole_training.x = df_pole_training.x.astype(float)
    df_pole_training.y = df_pole_training.y.astype(float)
    
    # Code형 데이터 One-Hot Encoding
    df_pole_training = pd.get_dummies(
        df_pole_training,
        columns=['pole_shape_cd', 'pole_type_cd', 'pole_spec_cd'],
        prefix=['pole_shape', 'pole_type', 'pole_spec']
    )
    # bool형 타입 데이터를 1과 0으로 변환
    df_pole_training = df_pole_training.applymap(
        lambda x: int(x) if isinstance(x, bool) else x
    )
    
    logs_pole.mid(f'제공받은 전주 데이터 학습 후 형태: {df_pole_training.shape}')
    if CFG.SAVE_INTERMEDIATE_FILE:
        write_data(
            CFG.PREPROCESS_DATA_INFO[dtype]['filename_all'],
            df_pole_training
        )    
        
    # 공사비의 공사번호를 기준으로 하나의 레코드 만들기
    # - 좌표값과 전주 순서는 여기서 처리하지 않고, 공사비당 각 코드별 합계 계산
    unique_cons_ids = df_pole_training.cons_id.unique()
    cons_id_row_values = []
    summation_columns = [
        col for col in df_pole_training.columns if col.startswith('pole_')
    ]
    # 공사번호별 각 코드의 사용 갯 수(합계)를 계산해 공사번호와 함께 리스트에 저장
    for cons_id in unique_cons_ids:
        df_curr = df_pole_training[df_pole_training.cons_id == cons_id]
        row_curr = df_curr[summation_columns].sum().values.tolist()
        cons_id_row_values.append([cons_id] + row_curr)
        
    df_pole_group = pd.DataFrame(
        cons_id_row_values, columns=['cons_id'] + summation_columns
    )
    
    df_training = pd.merge(
        df_training, df_pole_group,
        left_on='cons_id', right_on='cons_id', how='left'
    )
    
    # 저장
    write_data(
        CFG.PREPROCESS_DATA_INFO[dtype]['filename'],
        df_training
    )
    
    logs_pole.stop(
        f'전주정보 전처리 후 최종 학습 데이터 형태: {df_training.shape}'
    )
    return df_training

def _preprocess_line(df_line, dtype, df_training):
    pass