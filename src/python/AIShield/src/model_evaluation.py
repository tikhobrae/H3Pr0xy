#Write New Parameter on Moudel
import joblib
from sklearn.metrics import classification_report
import numpy as np
from data_preprocessing import preprocess_data

model = joblib.load('models/proxy_detection_rf_model.pkl')
X_new, y_new = preprocess_data('data/preprocessed_data.csv')
y_pred = model.predict(X_new)
print(classification_report(y_new, y_pred))
