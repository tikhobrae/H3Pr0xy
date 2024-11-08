#prediction
import joblib
import numpy as np
from data_preprocessing import preprocess_data

model = joblib.load('models/proxy_detection_rf_model.pkl')

new_data = np.array([[64, 150, 0]])
prediction = model.predict(new_data)
print(f"Prediction: {'Proxy' if prediction[0] == 1 else 'Not Proxy'}")
