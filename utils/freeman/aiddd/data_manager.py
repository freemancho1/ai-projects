import os
import warnings
import pandas as pd

BASE_DATA_PATH = os.path.join(os.path.expanduser('~'), 'projects', 'data', 'AIDDD')

def get_path(filename, data_type='preprocess', process_seq='3rd'):
    file_extension = '.xlsx' if data_type=='provide' else '.csv'
    dir_name = 'preprocessed_data' if data_type=='preprocess' else 'provided_data'
    full_path = [BASE_DATA_PATH, process_seq, dir_name, f'{filename}{file_extension}']
    return os.path.join(*full_path), file_extension

IS_USER_WARNING_SETTING = False

def read_data(filename, data_type='preprocess', process_seq='3rd', **kwargs):
    global IS_USER_WARNING_SETTING
    if not IS_USER_WARNING_SETTING:
        IS_USER_WARNING_SETTING = True
        # 엑셀파일을 읽을 때, openpyxl라이브러리에서 스타일관련 오류를 출력하는데, 
        # 일반적으로 이 경고는 무시해도 무방하기 때문에 설정을 변경함
        warnings.filterwarnings(
            'ignore',
            category=UserWarning,
            module='openpyxl.styles.stylesheet'
        )
        
    full_path, file_extension = get_path(filename, data_type, process_seq)
    if file_extension.lower() == '.xlsx':
        return pd.read_excel(full_path, **kwargs)
    else:
        return pd.read_csv(full_path, **kwargs)
    
def write_data(filename, dataframe, process_seq='3rd', **kwargs):
    full_path, _ = get_path(filename, 'preprocess', process_seq)
    if 'index' not in kwargs:
        kwargs['index'] = False
    dataframe.to_csv(full_path, **kwargs)
    
common_columns = {
    '공사번호': 'cons_id',              # Construction ID
    '총공사비': 'total_cons_cost',      # Total Construction Cost
    '최종변경일시': 'last_mod_date',    # Last Modification Date and Time
    '최종변경자사번': 'last_mod_eid',   # Last Modification Employee ID
    '사업소명': 'office_name',
    '계약전력': 'cont_cap',             # Contracted Capacity
    '전산화번호': 'comp_id',
    '전원측전산화번호': 'from_comp_id',
    'GISID': 'gis_id',
    '전주형태코드': 'pole_shape_cd',
    '전주종류코드': 'pole_type_cd',
    '전주규격코드': 'pole_spec_cd',
    'X좌표-Y좌표': 'coordinate', 
    '결선방식코드': 'wiring_scheme',
    '지지물간거리': 'span',
    '전선종류코드1': 'line_type_cd',
    '전선규격코드1': 'line_spec_cd',
    '전선조수1': 'line_phase_cd',
    '중성선종류코드': 'neutral_type_cd',
    '중성선규격코드': 'neutral_spec_cd',
    '인입전선종류코드': 'sl_type_cd',
    '고객공급선규격코드': 'sl_spec_cd',
    '조수': 'supervisor',
}