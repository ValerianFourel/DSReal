
import numpy as np
import matplotlib.pyplot as plot
import pandas as pnd

from keras.models import Sequential
from keras.layers import Dense


from keras.layers import LSTM as lest
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler as MMS


# taking in the set for training
dataSetTrain = pnd.read_csv('GSPTrain.csv')
SetTrain = dataSetTrain.iloc[:, 1:2].values

# Features ofor the scale
sc = MMS(feature_range = (0, 1))
SetTrain_scaled = sc.fit_transform(SetTrain)

trainedTime = []
trainedPrice = []
for i in range(60, 500):
    trainedTime.append(SetTrain_scaled[i-60:i, 0])
    trainedPrice.append(SetTrain_scaled[i, 0])
trainedTime, trainedPrice = np.array(trainedTime), np.array(trainedPrice)

# Reshaping
trainedTime = np.reshape(trainedTime, (trainedTime.shape[0], trainedTime.shape[1], 1))



# Creating the RNN


# RNN init
regFunction = Sequential()

# Adding the first lest layer and some Dropout regularisation
regFunction.add(lest(units = 50, return_sequences = True, input_shape = (trainedTime.shape[1], 1)))
regFunction.add(Dropout(0.15))

regFunction.add(lest(units = 50, return_sequences = True))
regFunction.add(Dropout(0.15))

regFunction.add(lest(units = 50, return_sequences = True))
regFunction.add(Dropout(0.15))

regFunction.add(lest(units = 50))
regFunction.add(Dropout(0.15))

#  output layer
regFunction.add(Dense(units = 1))

# RNN function
regFunction.compile(optimizer = 'adam', loss = 'mean_squared_error')

regFunction.fit(trainedTime, trainedPrice, epochs = 100, batch_size = 32)


dataset_test = pnd.read_csv('GOOGTest.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

dataset_total = pnd.concat((dataSetTrain['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regFunction.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)


# Representation
plot.plot(predicted_stock_price, color = 'green', label = 'Predicted Google Stock Price')

plot.plot(real_stock_price, color = 'purple', label = 'Real Google Stock Price')
plot.title('Prediction on the GOOG Price')
plot.xlabel('Time')
plot.ylabel('Google Stock Actual Price')
plot.legend()
plot.show()
