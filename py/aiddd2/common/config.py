import os

# 로그 관련
IS_DEBUG_MODE = True

# 중간에 생성된 파일 저장 여부
SAVE_INTERMEDIATE_FILE = True

# 데이터 위치
BASE_DATA_PATH = os.path.join(
    os.path.expanduser('~'), 'projects', 'data', 'AIDDD', 'curr_data'
)

# 제공받은 데이터 종류
DATA_TYPE = ['cons', 'pole', 'line', 'sl']
DATA_INFO = {
    'cons': {
        'filename': 'CONS_INFO.xlsx',
        'pp-filename': 'cons.csv',
        'pp-filename-temp': 'cons-temp.csv',
    }, 
    'pole': {
        'filename': 'POLE_DATA.xlsx',
        'pp-filename': 'pole.csv',
        'merge': 'merge-cp.csv',
    },
    'line': {
        'filename': 'LINE_DATA.xlsx',
        'pp-filename': 'line.csv',
        'merge': 'merge-cpl.csv',
    },
    'sl': {
        'filename': 'SL_DATA.xlsx',
        'pp-filename': 'sl.csv',
        'merge': 'merge-cpls.csv',
    },
    'count': {
        'pp-filename': 'facilities-count.csv',
        'pp-filename-temp': 'facilities-count-temp.csv',
    },
    'seqs': {
        'pp-filename': 'merge-cpls-path.csv'
    }
}

# 학습에 사용될 중요 변수
CURR_PROCESS_SEQ = '5th'
COND_ACC_TYPE_NAME = '신설(상용/임시)' 
COND_MAX_CONT_CAP = 50
COND_CONS_TYPE_CD = 2
COND_MAX_TOTAL_CONS_COST = 30000000
COND_MIN_POLE_COUNT = 1
COND_MIN_LINE_COUNT = 1
COND_MAX_POLE_COUNT = 10
COND_MAX_LINE_COUNT = 11

COMMON_COLUMNS = {
    '공사번호': 'cons_id',              # Construction ID
    '총공사비': 'total_cons_cost',      # Total Construction Cost
    '최종변경일시': 'last_mod_date',    # Last Modification Date and Time
    '최종변경자사번': 'last_mod_eid',   # Last Modification Employee ID
    '사업소명': 'office_name',
    '계약전력': 'cont_cap',             # Contracted Capacity
    '접수종류명': 'acc_type_name',      # Accept Type Name
    '공사형태코드': 'cons_type_cd',     # Construction Type Code
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
