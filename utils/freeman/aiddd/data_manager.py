import os
import warnings
import pandas as pd

DATA_BASE_PATH = os.path.join(
    os.path.expanduser('~'),
    'projects',
    'data',
    'AIDDD'
)

# cons: 공사비, line: 전선, pole: 전주, sl: service line(인입선)
PROVIDED_DATA_FILES = {
    # 2차: 공사비, 전주/전선/인입주
    '2nd provide cons': ['2nd', 'provided_data', 'CONS_INFO.xlsx'],
    '2nd provide line': ['2nd', 'provided_data', 'LINE_DATA.xlsx'],
    '2nd provide pole': ['2nd', 'provided_data', 'POLE_DATA.xlsx'],
    '2nd provide sl':   ['2nd', 'provided_data', 'SL_DATA.xlsx'],
    # 3차: 전주/전선/인입주
    '3rd provide line': ['3rd', 'provided_data', 'LINE_DATA.xlsx'],
    '3rd provide pole': ['3rd', 'provided_data', 'POLE_DATA.xlsx'],
    '3rd provide sl':   ['3rd', 'provided_data', 'SL_DATA.xlsx'],
} 

PREPROCESSED_DATA_FILES = {
    # 2nd: ba-pp-cons.ipynb
    '2nd pp cons-1st': ['2nd', 'preprocessed_data', 'cons-1st.csv'],
    '2nd pp cons-1st-all': ['2nd', 'preprocessed_data', 'cons-1st-all.csv'],
    # 2nd: bb-pp-device-counts-base-on-cons.ipynb <- '2nd pp cons-1st'
    '2nd pp counts-base-on-cons-1st': ['2nd', 'preprocessed_data', 'counts-base-on-cons-1st.csv'],
    # 2nd: bc-pp-pole-position-base-on-cons.ipynb <- '2nd pp counts-base-on-cons-1st'
    '2nd pp pole-position-on-cons-1st': ['2nd', 'preprocessed_data', 'pole-position-base-on-cons-1st.csv'],
    
    # 2nd vs 3rd: 전처리 후 컬럼명 영문으로 변경, 좌표값
    # 3rd: ba-pp-cons.ipynb
    '3rd pp cons-1st': ['3rd', 'preprocessed_data', 'cons-1st.csv'],
    '3rd pp cons-1st-all': ['3rd', 'preprocessed_data', 'cons-1st-all.csv'],
    # 3rd: bb-pp-device-counts-base-on-cons.ipynb <- '3rd pp cons-1st'
    '3rd pp counts-base-on-cons-1st': ['3rd', 'preprocessed_data', 'counts-base-on-cons-1st.csv'],
    # 3rd: bc-pp-pole-position-base-on-cons.ipynb <- '3rd pp counts-base-on-cons-1st'
    '3rd pp pole-position-on-cons-1st': ['3rd', 'preprocessed_data', 'pole-position-base-on-cons-1st.csv'],
}

# DATA_FILES = PROVIDED_DATA_FILES + PREPROCESSED_DATA_FILES
DATA_FILES = PROVIDED_DATA_FILES
DATA_FILES.update(PREPROCESSED_DATA_FILES)

def get_path(file_key):
    try:
        file_path = DATA_FILES[file_key]
    except KeyError as ke:
        raise KeyError(f'Key of File `{file_key}` does not Exist.')
    joined_path = [DATA_BASE_PATH] + file_path
    return os.path.join(*joined_path)

IS_USER_WARNING_SETTING = False

def read_data(file_key, **kwargs):
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
    
    read_file_path = get_path(file_key)
    file_extension = os.path.splitext(read_file_path)[1]
    if file_extension.lower() == '.xlsx':
        return pd.read_excel(read_file_path, **kwargs)
    else:
        return pd.read_csv(read_file_path, **kwargs)
    
def write_data(file_key, dataframe, **kwargs):
    write_file_path = get_path(file_key)
    if 'index' not in kwargs:
        kwargs['index'] = False
    dataframe.to_csv(write_file_path, **kwargs)
    