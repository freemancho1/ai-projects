import os
import warnings
import pandas as pd


_PATH_BASE = os.path.join(os.path.expanduser('~'), 'projects', 'data', 'AIDDD')

def _get_path(*paths):
    path = [_PATH_BASE] + [_path for _path in paths]
    return os.path.join(*path)

_PATH_READ_FILES = {
    'kbt 고객':     _get_path('1st', 'KBT(설비)', 'KBT(설비) 추출내역', 'KBT 저압고객 추출내역.xlsx'),
    'kbt 인입선':   _get_path('1st', 'KBT(설비)', 'KBT(설비) 추출내역', 'KBT 저압인입선 추출내역.xlsx'),
    'kbt 장주애자': _get_path('1st', 'KBT(설비)', 'KBT(설비) 추출내역', 'KBT 저압장주애자 추출내역.xlsx'),
    'kbt 전선':     _get_path('1st', 'KBT(설비)', 'KBT(설비) 추출내역', 'KBT 저압전선 추출내역.xlsx'),
    'kbt 전주':     _get_path('1st', 'KBT(설비)', 'KBT(설비) 추출내역', 'KBT 전주 추출내역.xlsx'),
    'kbt 접지':     _get_path('1st', 'KBT(설비)', 'KBT(설비) 추출내역', 'KBT 접지 추출내역.xlsx'),
    'kbt 지지선':   _get_path('1st', 'KBT(설비)', 'KBT(설비) 추출내역', 'KBT 지지선 추출내역.xlsx'),
    # '공사비':     _get_path('1st', '공사비예산서', '5개년 공사비 예산서 추출내역.xlsx'),
    '공사비':       _get_path('1st', '공사비예산서', '5개년 공사비 예산서 추출내역_계약전력등추가.xlsx'),
    '공사비 공사비': _get_path('1st', '공사비예산서', '5개년 공사비 예산서 추출내역_계약전력등추가.xlsx'),
    '기별 애자':    _get_path('1st', '기별', '추출내역', '계약전력등추가', '5개년 저압애자_기별(자재,품,해설_기계경비) 추출내역_계약전력등추가.xlsx'),
    '기별 인입선':  _get_path('1st', '기별', '추출내역', '계약전력등추가', '5개년 저압인입선_기별(자재,품,해설_기계경비) 추출내역_계약전력등추가.xlsx'),
    '기별 장주':    _get_path('1st', '기별', '추출내역', '계약전력등추가', '5개년 저압장주_기별(자재,품,해설_기계경비) 추출내역_계약전력등추가.xlsx'),
    '기별 전선':    _get_path('1st', '기별', '추출내역', '계약전력등추가', '5개년 저압전선_기별(자재,품,해설_기계경비) 추출내역_계약전력등추가.xlsx'),
    '기별 전주':    _get_path('1st', '기별', '추출내역', '계약전력등추가', '5개년 전주_기별(자재,품,해설_기계경비) 추출내역_계약전력등추가.xlsx'),
    '기별 접지':    _get_path('1st', '기별', '추출내역', '계약전력등추가', '5개년 접지_기별(자재,품,해설_기계경비) 추출내역_계약전력등추가.xlsx'),
    '기별 지지선':  _get_path('1st', '기별', '추출내역', '계약전력등추가', '5개년 지지선_기별(자재,품,해설_기계경비) 추출내역_계약전력등추가.xlsx'),
    '설계 고객':    _get_path('1st', '설계', '설계 추출내역', '계약전력등추가', '5개년 저압고객 설계 추출내역_계약전력등추가.xlsx'),
    '설계 애자':    _get_path('1st', '설계', '설계 추출내역', '계약전력등추가', '5개년 저압애자 설계 추출내역_계약전력등추가.xlsx'),
    '설계 인입선':  _get_path('1st', '설계', '설계 추출내역', '계약전력등추가', '5개년 저압인입선 설계 추출내역_계약전력등추가.xlsx'),
    '설계 장주':    _get_path('1st', '설계', '설계 추출내역', '계약전력등추가', '5개년 저압장주 설계 추출내역_계약전력등추가.xlsx'),
    '설계 전선':    _get_path('1st', '설계', '설계 추출내역', '계약전력등추가', '5개년 저압전선 설계 추출내역_계약전력등추가.xlsx'),
    '설계 전주':    _get_path('1st', '설계', '설계 추출내역', '계약전력등추가', '5개년 전주 설계 추출내역_계약전력등추가.xlsx'),
    '설계 접지':    _get_path('1st', '설계', '설계 추출내역', '계약전력등추가', '5개년 접지 설계 추출내역_계약전력등추가.xlsx'),
    '설계 지지선':  _get_path('1st', '설계', '설계 추출내역', '계약전력등추가', '5개년 지지선 설계 추출내역_계약전력등추가.xlsx'),
    '2ndCONS': _get_path('2nd', 'soc', 'CONS_INFO.xlsx'),
    '2ndLINE': _get_path('2nd', 'soc', 'LINE_DATA.xlsx'),
    '2ndPOLE': _get_path('2nd', 'soc', 'POLE_DATA.xlsx'),
    '2ndSL': _get_path('2nd', 'soc', 'SL_DATA.xlsx'),
}

_PATH_READ_WRITE_FILES = {
    '1st통계 전체': _get_path('1st', '전처리데이터', '통계 전체.csv'),
    '1st통계 1st전처리': _get_path('1st', '전처리데이터', '통계 1st전처리.csv'),
    '1st통계 2차전처리': _get_path('1st', '전처리데이터', '통계 2차전처리.csv'),
    '1st병합 전체카운트': _get_path('1st', '전처리데이터', '병합 전체카운트.csv'),
    '1st전처리 공사비': _get_path('1st', '전처리데이터', '전처리공사비.csv'),
    '1st전처리 공사비+설계': _get_path('1st', '전처리데이터', '전처리공사비_설계.csv'),
    '1st전처리 공사비+설계기별': _get_path('1st', '전처리데이터', '전처리공사비_설계기별.csv'),
    # '전처리 설계전선': _get_path('전처리데이터', '전처리 설계전선.csv'),
    # '전처리 설계전주': _get_path('전처리데이터', '전처리 설계전주.csv'),
    '2nd stats': _get_path('2nd', 'pp', 'stats_all.csv'),
    '2nd stats_target': _get_path('2nd', 'pp', 'stats_target.csv')
}

_IS_SETTING = False

def read_data(type, nrows=None):
    global _IS_SETTING
    
    if _IS_SETTING == False:
        _IS_SETTING = True
        # 엑셀파일을 읽을 때, openpyxl라이브러리에서 스타일관련 오류를 출력하는데, 
        # 일반적으로 이 경고는 무시해도 무방하기 때문에 설정을 변경함
        warnings.filterwarnings(
            'ignore',
            category=UserWarning,
            module='openpyxl.styles.stylesheet'
        )
    
    try:
        file_path = _PATH_READ_FILES[type]
    except KeyError as ke:
        file_path = _PATH_READ_WRITE_FILES[type]
        
    # 파일확장자를 비교해 읽는 함수를 결정
    file_ext = os.path.splitext(file_path)[1]
    return pd.read_excel(file_path, nrows=nrows) if file_ext.lower() == '.xlsx' \
        else pd.read_csv(file_path, nrows=nrows)
    
# get_data = lambda type: pd.read_excel(_PATH_FILES[type])

def write_data(type, df, index=False):
    # 전처리 이후 파일은 무조건 csv파일로 관리
    df.to_csv(_PATH_READ_WRITE_FILES[type], index=index)