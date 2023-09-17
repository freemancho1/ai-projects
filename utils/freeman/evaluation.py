import numpy as np

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score

import matplotlib.pyplot as plt

def user_mape(y_test, pred):
    max_value = max(np.max(y_test), 1)
    mape = 0
    
    data_size = len(y_test)
    
    for i in range(data_size):
        (y, p) = (max_value, pred[i]+max_value) if y_test[i] < 1 else (y_test[i], pred[i])
        mape += abs((y-p) / y) * 100
        
    return mape / data_size

def regression_evaluation(y_test, pred, verbose=1):
    # 모든값을 소숫점 5자리에서 반올림(np 자체의 버그인지 일단 해결하기 위함)
    y = np.round(y_test, decimals=5)
    p = np.round(pred, decimals=5)
    
    mse = mean_squared_error(y, p)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, p)
    r2score = r2_score(y, p)
    mape = mean_absolute_percentage_error(y, p)
    # mape2 = user_mape(y, p)
    
    if verbose != 0:
        print(
            f'R2_SCORE: {r2score:.6f}, MAPE: {mape*100:.6f}, '
            f'MSE: {mse:.6f}, RMSE: {rmse:.6f}, '
            f'MAE: {mae:.6f}'
        )
        
    return [r2score, mape, mse, rmse, mae]

def f_importances(model, columns, title):
    _f_importances = model.feature_importances_

    plt.figure(figsize=(12,12))
    plt.barh(range(len(_f_importances)), _f_importances)
    plt.yticks(range(len(_f_importances)), columns)
    plt.xlabel('중요도')
    plt.ylabel('속성')
    plt.title(f'{title} 속성별 중요도')
    plt.show()
    
def plot_actual_pred(y_test, pred, title):
    plt.figure(figsize=(12,6))
    x = range(len(y_test))
    plt.plot(x, y_test, label='실측값', linestyle='-')
    plt.plot(x, pred, label='예측값', linestyle='--')
    plt.xlabel('공사 단위')
    plt.ylabel('총공사비')
    plt.title(title)
    plt.legend()
    plt.show()