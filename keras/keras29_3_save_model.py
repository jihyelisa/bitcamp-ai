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

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input

input1 = Input(shape=(13,))
dense1 = Dense(40, activation='relu')(input1)
dense2 = Dense(50, activation ='relu')(dense1)
dense3 = Dense(50, activation ='relu')(dense2)
dense4 = Dense(60, activation ='relu')(dense3)
dense5 = Dense(60, activation ='relu')(dense4)
dense6 = Dense(10)(dense5)
output1 = Dense(1)(dense6)
model = Model(inputs=input1, outputs=output1)

path = './_save/'
# model.save(path + 'keras29_1_save_model.h5')


##3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

earlyStopping = EarlyStopping(monitor="val_loss",
                              mode="min", patience=5, restore_best_weights=True)

hist = model.fit(x_train, y_train, epochs=300, batch_size=1,
          validation_split=0.2, callbacks=[earlyStopping], verbose=3)

# 컴파일 훈련 이후에 save 해보기
model.save(path + 'keras29_3_save_model.h5')
# 결과 R2: 0.7613947702009047


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