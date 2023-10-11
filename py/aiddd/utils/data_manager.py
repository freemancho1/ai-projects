import os
import pandas as pd

from aiddd.app import config as CFG

def get_path(filename, data_type, process_seq):
    full_path = [
        CFG.BASE_DATA_PATH, process_seq, CFG.DATA_PATH[data_type], filename
    ]
    return os.path.join(*full_path)

def read_data(
    filename,
    data_type='preprocessed',
    process_seq=CFG.CURR_PROCESS_SEQ,
    **kwargs
):
    full_path = get_path(filename, data_type, process_seq)
    _, file_extension = os.path.splitext(full_path)

    if file_extension.lower() == '.xlsx':
        return pd.read_excel(full_path, **kwargs)
    elif file_extension.lower() == '.csv':
        return pd.read_csv(full_path, **kwargs)
    else:
        raise ValueError(
            f'파일확장자 에러: {file_extension}(확장자는 `xlsx, csv`만 가능)'
        )

def write_data(filename, df, process_seq=CFG.CURR_PROCESS_SEQ, **kwargs):
    full_path = get_path(filename, 'preprocessed', process_seq)
    if 'index' not in kwargs:
        kwargs['index'] = False
    df.to_csv(full_path, **kwargs)

def get_rename_columns(columns):
    return {
        column_name: CFG.COMMON_COLUMNS[column_name]
        for column_name in CFG.COMMON_COLUMNS \
            if column_name in columns
    }