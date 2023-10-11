from datetime import datetime
from aiddd.app import config as CFG
from aiddd.utils.logs import Log
from aiddd.utils.data_manager import read_data, get_rename_columns

logs = Log()

def get_provide_data():
    logs.start('제공받은 데이터 불러오기 시작...')

    provide_data = {}
    for data_info in CFG.PROVIDE_DATA:
        start_time = datetime.now()
        filename = CFG.PROVIDE_DATA_INFO[data_info]['filename']
        curr_df = read_data(
            filename, data_type='provided',
            process_seq=CFG.PROVIDE_DATA_INFO[data_info]['process_seq']
        )
        # 학습에 사용할 주요 컬럼명을 영문으로 변경
        curr_df.rename(columns=get_rename_columns(curr_df.columns), inplace=True)
        logs.mid(
            f'읽은 파일: {filename}, 데이터 형태: {curr_df.shape}, '
            f'처리 시간: {datetime.now() - start_time}'
        )
        provide_data[data_info] = curr_df

    logs.stop('제공받은 데이터 불러오기 종료...')
    return provide_data