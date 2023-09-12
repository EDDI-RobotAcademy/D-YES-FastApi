import numpy as np
from tensorflow import keras
def get_predict_price(agriculture_name, temp_list, rain_list, price_list):

    X_temp = temp_list
    X_rain = rain_list
    X_price = price_list

    window_size = 3

    model_choice = agriculture_name # something methods choice model
    model = keras.models.load_model("D:/teamProject/D-YES-FastApi/app/model_running/cabbage_model.h5")

    predictions = []

    for i in range(len(X_temp) - window_size):

        _X_temp = X_temp[i: i + window_size]
        _X_rain = X_rain[i: i + window_size]
        _X_price = X_price[i: i + window_size]

        current_data = []
        data_X = []

        for j in range(window_size):
            current_data.append([_X_temp[j], _X_rain[j], _X_price[j]])

        data_X.append(current_data)

        data_X_reshape = np.array(data_X).reshape(-1, 3, 3)

        prediction = model.predict(data_X_reshape)
        prediction=prediction[0][0]

        predictions.append(prediction)
        X_price.append(prediction)
        
    return predictions