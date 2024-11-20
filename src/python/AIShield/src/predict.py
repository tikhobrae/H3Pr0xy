import joblib
import numpy as np
from data_preprocessing import preprocess_data

def load_model(model_path):
    """Load a trained model from a file."""
    try:
        model = joblib.load(model_path)
        print("Model loaded successfully.")
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {model_path}.")

def predict_proxy(model, data):
    """Predict if the given data point is a proxy or not."""
    # Check data format
    if data.ndim == 1:
        data = data.reshape(1, -1)
    
    prediction = model.predict(data)
    return "Proxy" if prediction[0] == 1 else "Not Proxy"

if __name__ == "__main__":
    model_path = 'models/proxy_detection_rf_model.pkl'
    model = load_model(model_path)

    # New Data For Test Here We have exam data
    new_data = np.array([64, 150, 0]) 
    
    result = predict_proxy(model, new_data)
    print(f"Prediction: {result}")