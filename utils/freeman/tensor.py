import sys
import numpy as np
import pandas as pd
import tensorflow as tf

class MakeWindow():
    
    def __init__(
        self,
        data,
        window_size,
        batch_size, 
        label_idx=None,  
        label_col=None,
        drop_col_label=False,
        last_idx_label=False,
        shift=1,
        prefetch_size=1,
        shuffle=False,
        drop_remainder=True
    ):
        self.data = data
        self.window_size = window_size
        self.batch_size = batch_size
        self.label_idx = label_idx
        self.label_col = label_col
        self.drop_col_label = drop_col_label
        self.last_idx_label = last_idx_label
        self.shift = shift
        self.prefetch_size = prefetch_size
        self.shuffle = shuffle
        self.drop_remainder = drop_remainder
        self.col_indices = None
        
        self._train_data = None
        self._valid_data = None
        self._test_data = None
        
        self._check_args()
        self._make_window()
        self.spec
        
    
    def _make_window(self):
        # 시작 레이블 위치를 윈도우 내면 -1 아니면 윈도우크기로 지정
        label_start_row = self.window_size
        label_start_row -= 1 if self.last_idx_label else 0
        
        # 학습데이터에 레이블 추가 또는 제거
        X = np.delete(self.data, self.label_idx, axis=1) \
            if self.drop_col_label else self.data
        y = self.data[:, self.label_idx]
        
        # 각각의 데이터셋 생성
        ds_X = tf.data.Dataset.from_tensor_slices(X)
        ds_y = tf.data.Dataset.from_tensor_slices(y[label_start_row:])
        
        # 윈도우 생성
        ds_X = ds_X.window(
            self.window_size, shift=self.shift, drop_remainder=self.drop_remainder
        )
        # 윈도우를 하나의 배치로 묶음
        ds_X = ds_X.flat_map(lambda w: w.batch(self.window_size))
        
        # 속성과 레이블을 묶음(shuffle을 할 때 같이 움직여야하기 때문)
        ds = tf.data.Dataset.zip((ds_X, ds_y))
        if self.shuffle:
            shuffle_size = int(self.data.shape[0] / self.batch_size)
            ds = ds.shuffle(shuffle_size)
            
        self.win_data = ds.batch(self.batch_size).prefetch(self.prefetch_size)
        
    def slices(self, size=[60, 20, 20]):
        len_size = len(size)
        if len_size == 1:
            if size[0] > 40 and size[0] < 90 :
                train_size = size[0]
                valid_size = 0
                test_size = 100 - size[0]
            else:
                self._display_error(
                    'The size of the training data should be between 40% and 90%\n'
                    f'Currently, the input value is `{size[0]}%`.'
                )
        elif len_size == 2:
            sum_size = np.sum(size)
            if sum_size == 100:
                train_size = size[0]
                valid_size = 0
                test_size = size[1]
            else:
                self._diplay_error(
                    'The size of the training and test data should sum up to 100%.\n'
                    f'Currently, the input values are {size[0]}% and {size[1]}%.'
                )
        elif len_size == 3:
            sum_size = np.sum(size)
            if sum_size == 100:
                train_size = size[0]
                valid_size = size[1]
                test_size = size[2]
            else:
                self._diplay_error(
                    'The size of the training, validation and test data should sum up to 100%.\n'
                    f'Currently, the input values are {size[0]}%, {size[1]}% and {size[2]}%.'
                )
        else:
            self._display_error(
                'Data splitting should involve three sets: training, validation and test data.\n'
                f'Currently, {len_size} sets have been input.'
            )
            
        _train_size = int(self.batch_data_size * train_size / 100)
        _valid_size = int(self.batch_data_size * valid_size / 100)
        _test_size = int(self.batch_data_size * test_size / 100)
        
        self._train_data = self.win_data.take(_train_size)
        _remaining_data = self.win_data.skip(_train_size)
        self._valid_data = _remaining_data.take(_valid_size)
        self._test_data = _remaining_data.skip(_valid_size)
        
        print('Train Data:')
        self._win_spec(self._train_data)
        if _valid_size != 0:
            print('Valid Data:')
            self._win_spec(self._valid_data)
        print('Test Data:')
        self._win_spec(self._test_data)
        
    def _win_spec(self, ds=None):
        batch_data_size = 0
        total_data_size = 0
        
        _ds = self.win_data if ds is None else ds
        
        for x, y in _ds.take(-1):
            if batch_data_size == 0:
                print(f'Batch dataset shape: features{x.shape}, label{y.shape}')
            batch_data_size += 1
            total_data_size += x.shape[0]
        
        print(
            f'Last batch dataset shape: features{x.shape}, label{y.shape}\n'
            f'Batch dataset size: {batch_data_size}\n'
            f'Total dataset row size: {total_data_size} = '
            f'{self.batch_size} * ({batch_data_size} - 1) + {x.shape[0]}'
        )
        
        if ds is None:
            self.batch_data_size = batch_data_size
            self.input_shape = x.shape[1:]
        
    @property
    def spec(self):
        self._win_spec()
        
    @property
    def train(self):
        if self._train_data is None:
            self.slices()
        return self._train_data
    
    @property
    def valid(self):
        if self._valid_data is None:
            self.slices()
        return self._valid_data
    
    @property
    def test(self):
        if self._test_data is None:
            self.slices()
        return self._test_data
    
    """
    _check_args(): 
        클래스에 입력된 인자를 체크하고, 최종적으로 처리할 데이터를 np.ndarray로 변환
        1. `label_idx`와 `label_col` 체크 (존재 여부)
        2. `last_idx_label` 상태에 따라 `drop_col_label` 상태 변경
        3. 처리할 데이터 점검(np.ndarray, pd.DataFrame 만 허용)
        4. `label_idx`와 `label_col` 체크 (값의 적절성)
    """
    def _check_args(self):
        
        # 윈도우의 마지막 로우에서 레이블을 가져올 경우,
        # 해당 레이블 컬럼은 자동으로 속성 컬럼에서 제거됩니다.
        # 윈도우 마지막 로우 다음 로우에서 레이블을 가져올 경우에는
        # 이전 레이블 컬럼이 속성에 포함될 수 도 있습니다.
        if self.last_idx_label:
            self.drop_col_label = True
        
        # 입력 데이터가 튜플인 경우
        if isinstance(self.data, tuple):
            _X, _y = self.data
            # 속성 데이터 타입 체크
            if not (isinstance(_X, np.ndarray) or isinstance(_X, pd.DataFrame)):
                self._display_error(
                    'The data type of features data can only `np.ndarray` or `pd.DataFrame`.\n'
                    f'The provided features data has a format of `{type(_X)}`.'
                )
            # 레이블 데이터 타입 체크(Series까지 추가)
            if not (isinstance(_y, np.ndarray) 
                        or isinstance(_y, pd.DataFrame) or isinstance(_y, pd.Series)):
                self._display_error(
                    'The data type of label data can only `np.ndarray`, `pd.DataFrame` or `pd.Series`.\n'
                    f'The provided label data has a format of `{type(_y)}`.'
                )
            # 데이터프레임과 시리즈일 경우 np.ndarray형으로 변환
            if isinstance(_X, pd.DataFrame):
                _X = _X.values
            if isinstance(_y, pd.DataFrame) or isinstance(_y, pd.Series):
                _y = _y.values
            
            # 속성 데이터 차원의 2차원 여부 체크
            if len(_X.shape) != 2:
                self._display_error(
                    'The attribute data must be a two-dimensional array, '
                    f'but the input data is {len(_X.shape)}-dimensional.'
                )
                
            # 레이블 데이터를 속성 데이터 마지막에 추가할 것이기 때문에,
            # 레이블 데이터 컬럼의 인덱스를 속성데이터의 속성 컬럼 갯 수로 지정
            # 아래 코드는 배열 (100, 8)과 (100,)를 컬럼으로 연결해 (100, 9)로 만드는 코드고
            # 여기서 추가된 9번째 컬럼의 인덱스가 8(처음 속성컬럼의 크기(shape[1])와 같음)
            self.label_idx = _X.shape[1]
            self.data = np.column_stack((_X, _y))
        
        # 데이터 타입이 배열과 데이터프레임인 경우 처리
        elif isinstance(self.data, np.ndarray) or isinstance(self.data, pd.DataFrame):
            # 레이블 컬럼과 컬럼 인덱스가 모두 없으면 안되니 체크
            if self.label_idx is None and self.label_col is None:
                self._display_error(
                    'You must specify either the label column name or the label column index, '
                    'and in case of duplicate specifications, the index takes precedence.'
                )
            # 데이터가 배열이면서 레이블 컬럼 인덱스가 없는지 체크
            if isinstance(self.data, np.ndarray) and self.label_idx is None:
                self._display_error(
                    'When processing an np.ndarray data, '
                    'you need to input the index of the label column directly.'
                )
            # 데이터가 데이터프레임인 경우 처리
            if isinstance(self.data, pd.DataFrame):
                # 레이블 컬럼명으로 레이블의 인덱스를 찾기 위해 모든 컬럼을 인덱싱함
                self.col_indices = {
                    name: i for i, name in enumerate(self.data.columns)
                }
                try:
                    # 레이블 컬럼명이 데이터프레임 컬럼명들 속에 있나 체크
                    self.label_idx = self.label_idx if self.label_idx is not None \
                        else self.col_indices[self.label_col]
                except KeyError as ke:
                    self._display_error(
                        'You have entered the label column name incorrectly. '
                        f'The column {ke} does not exist.'
                    )
                    
                # 레이블 컬럼 인덱스 등 데이터프레임으로 할 작업을 모두 종료했기 때문에
                # self.data를 np.ndarray로 변환
                self.data = self.data.values
        else:
            self._display_error(
                'The acceptable data formats are `np.ndarray` or `pd.DataFrame`.\n'
                f'The provided data has a format of `{type(self.data)}`.'
            )
                        
        if self.label_idx < 0:
            self._display_error(
                f'The label index must be greater than 0. Input value: {self.label_idx}'
            )
        if self.label_idx >= self.data.shape[1]:
            self._display_error(
                'The label index cannot exceed the total number of columns.\n'
                f'Input label index: {self.label_idx}, '
                f'Total number of columns: {self.data.shape[1]}'
            )
            
    def _display_error(self, message):
        self = None
        raise ValueError(message)
    
# wd: window data
# sd: source data
# ws: window size
# bs: batch size
# tidx: target column index
# dcol: drop target column (bool)
# lidx: get target in window last row (bool)
def check_window_data(wd, sd, ws, bs, tidx, dcol, lidx):
    is_match = True
    idx = 0
    X_data = np.delete(sd, tidx, axis=1) if dcol else sd 
    y_data = sd[ws-1 if lidx else ws:, tidx]
    
    for x, y in wd.take(-1):
        idxx1 = 0
        for xe in x:
            idxx2 = 0
            for xee in xe.numpy():
                if np.all(X_data[idx*bs+idxx1+idxx2] != xee):
                    print(f'Not match X({idx}, {idxx1}, {idxx2}): \n{X_data[idx*bs+idxx1+idxx2]}\n{xee}')
                    is_match = False
                idxx2 += 1
            idxx1 += 1
        idxy = 0
        for ye in y:
            if np.all(y_data[idx*bs+idxy]!=ye):
                print(f'Not match y({idx}, {idxy}): {y_data[idx*bs+idxy]}, {ye}')    
                is_match = False
            idxy += 1   
        idx += 1     
        if not is_match:
            print('Not Match')
            break
        
    if is_match:
        print('Match')

def dataset_spec(ds):
    batch_data_size = 0
    total_data_size = 0
    try:
        for x, y in ds.take(-1):
            if batch_data_size == 0:
                print(f'Data shape: {x.shape}, {y.shape}', end=', ')
            batch_data_size += 1
            total_data_size += x.shape[0]
        print(f'Last data shape: {x.shape}, {y.shape}')
        print(f'Batch data size: {batch_data_size}, Total data size: {total_data_size}')
    except ValueError as ve:
        for x in ds.take(-1):
            if batch_data_size == 0:
                print(f'Data shape: {x.shape}', end=', ')
            batch_data_size += 1
            total_data_size += x.shape[0]
        print(f'Last data shape: {x.shape}')
        print(f'Batch data size: {batch_data_size}, Total data size: {total_data_size}')
    except TypeError as te:
        for x in dataset:
            if batch_data_size == 0: 
                print('Data shape: 1')
            batch_data_size += 1
        print(f'Batch data size: {batch_data_size}') 