import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint



##1. 데이터
path = './_data/ddarung/'
train_csv = pd.read_csv(path + 'train.csv', index_col=0)
test_csv = pd.read_csv(path + 'test.csv', index_col=0)
submission = pd.read_csv(path + 'submission.csv', index_col=0)

train_csv = train_csv.dropna()
x = train_csv.drop(['count'], axis=1)   #칼럼의 축 axis
y = train_csv['count']
x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.9, random_state=209)

from sklearn.preprocessing import MinMaxScaler, StandardScaler
scaler = MinMaxScaler()
# scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
# fit은 기준을 정하는 느낌?? 한 번만 해준다
x_test = scaler.transform(x_test)

print(x_train.shape, x_test.shape)  # (1195, 9) (133, 9)
x_train = x_train.reshape(1195, 3, 3)
x_test = x_test.reshape(133, 3, 3)


##2. 모델구성
model = Sequential()
model.add(LSTM(40, activation ='relu', input_shape=(3, 3)))
model.add(Dropout(0.3))
model.add(Dense(50, activation="relu"))
model.add(Dense(50, activation="relu"))
model.add(Dense(100, activation="relu"))
model.add(Dense(50, activation="relu"))
model.add(Dense(1))


##3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam')

earlyStopping = EarlyStopping(monitor="val_loss",
                              mode="min", patience=5, restore_best_weights=True)

import datetime
date = datetime.datetime.now()
date = date.strftime("%m%d_%H%M")  # 현재 날짜와 시간
filepath = './_save/MCP/'
filename = '{epoch:04d}-{val_loss:.4f}.hdf5'    # 0037-0.0048.hdf5

mcp = ModelCheckpoint(monitor='val_loss', mode='auto',
                      verbose=1, save_best_only=True,
                      filepath=filepath + 'ddarung_LSTM_' + date + '_' + filename)

model.fit(x_train, y_train, epochs=200, batch_size=20,
          validation_split=0.1, callbacks=[earlyStopping, mcp], verbose=3)


##4. 평가, 예측
loss = model.evaluate(x_test, y_test)
print('loss:', loss)

y_predict = model.predict(x_test)
def RMSE(y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE:", RMSE(y_test, y_predict))

r2 = r2_score(y_test, y_predict)
print("R2:", r2)


##5. 제출 파일
test_csv = scaler.transform(test_csv)
# scaler 이용해 0~1 사이값으로 얻은 웨이트값이므로 제출파일 만들 때도 scaler 해준 뒤 예측한다
# print(test_csv.shape)  # (715, 9)
test_csv = test_csv.reshape(715, 3, 3)

submission['count'] = model.predict(test_csv)
submission.to_csv(path + 'submission_0125_.csv')



'''
loss: 2536.46728515625
RMSE: 50.36335215390803
R2: 0.6587549735600373
'''