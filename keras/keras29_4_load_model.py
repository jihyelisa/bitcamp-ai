from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping


##1. 데이터
dataset = load_boston()
x = dataset.data
y = dataset['target']

x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.7, random_state=20)

from sklearn.preprocessing import MinMaxScaler, StandardScaler

scaler = MinMaxScaler()
# scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


##2. 함수형 모델구성

from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Dense, Input

path = './_save/'
model = load_model(path + 'keras29_3_save_model.h5')
# 결과 R2: 0.7613947702009047

# 컴파일, 훈련 이후에 model.save 하면 가중치까지 저장됨!
# load_model 했을 때 결과가 완전히 같음!


##3. 컴파일, 훈련


##4. 평가, 예측
mse, mae = model.evaluate(x_test, y_test)
print('mse:', mse, ' / mae:', mae)

y_predict = model.predict(x_test)
# print(y_test)
# print(y_predict)

from sklearn.metrics import mean_squared_error, r2_score
def RMSE(y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE:", RMSE(y_test, y_predict))

r2 = r2_score(y_test, y_predict)
print("R2:", r2)