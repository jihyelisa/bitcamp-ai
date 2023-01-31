import numpy as np

x_train = np.load('./_data/dogs-vs-cats/dog_cat_x_train_100.npy')
y_train = np.load('./_data/dogs-vs-cats/dog_cat_y_train_100.npy')
# x_test = np.load('./_data/dogs-vs-cats/dog_cat_x_test_100.npy')
# y_test = np.load('./_data/dogs-vs-cats/dog_cat_y_test_100.npy')
test_img = np.load('./_data/dogs-vs-cats/test_img.npy')

# print(x_train.shape, y_train.shape)
# (25000, 100, 100, 3) (25000,)
# print(x_test.shape, y_test.shape)
# (12500, 100, 100, 3) (12500,)



##2. 모델
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten

model = Sequential()
model.add(Conv2D(30, 30, input_shape=(100, 100, 3)))
model.add(Conv2D(80, 20, activation='relu'))
model.add(Conv2D(40, 20, activation='relu'))
model.add(Flatten())
model.add(Dense(20, activation='relu'))
model.add(Dense(1, activation='sigmoid'))



##3. 컴파일, 훈련
model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['acc'])

hist = model.fit(x_train, y_train,
                 batch_size=80, epochs=5,
                 validation_split=0.2,
                 verbose=3)



##4. 평가, 예측
# loss = hist.history['loss']
# val_loss = hist.history['val_loss']
accuracy = hist.history['acc']
val_acc = hist.history['val_acc']

# print('loss:', loss[-1])
# print('val_loss:', val_loss[-1])
print('accuracy:', accuracy[-1])
print('val_acc:', val_acc[-1])


test = model.predict(test_img)
if test == 0:
    print('cat')
else:
    print('dog')


'''
loss: 3.6270205328037264e-06
val_loss: 0.023630639538168907
accuracy: 1.0
val_acc: 0.9916666746139526
'''