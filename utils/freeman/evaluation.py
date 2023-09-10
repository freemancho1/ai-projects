import numpy as np

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score

import matplotlib.pyplot as plt

def user_mape(y_test, pred):
    # 예측대상(test_y)값이 0인 경우를 대비해, 
    # 0이 아닌 아주 작은수를 더해 MAPE값을 구함
    epsilon = 1e-10
    
    abs_err = np.abs(y_test - pred)
    y_test = y_test + epsilon
    
    pct_err = np.where(abs_err == 0, 0, abs_err / y_test * 100) 

    # for i in range(len(pct_err)):
    #     if pct_err[i] > 100:
    #         print(y_test[i], pred[i], pct_err[i])
    pct_err = np.minimum(pct_err, 100)
    
    return np.mean(pct_err)

def regression_evaluation(y_test, pred, verbose=1):
    # 모든값을 소숫점 5자리에서 반올림(np 자체의 버그인지 일단 해결하기 위함)
    y = np.round(y_test, decimals=5)
    p = np.round(pred, decimals=5)
    
    mse = mean_squared_error(y, p)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, p)
    r2score = r2_score(y, p)
    mape = mean_absolute_percentage_error(y, p)
    mape2 = user_mape(y, p)
    
    if verbose != 0:
        print(
            f'R2_SCORE: {r2score:.6f}, MAPE2: {mape2:.6f}, '
            f'MSE: {mse:.6f}, RMSE: {rmse:.6f}, '
            f'MAPE: {mape:.6f}, MAE: {mae:.6f}'
        )
        
    return mse, rmse, mae, mape, mape2

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