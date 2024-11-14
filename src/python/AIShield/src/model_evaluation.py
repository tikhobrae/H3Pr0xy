import joblib
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
from data_preprocessing import preprocess_data

def load_model(model_path):
    """Load and return a pre-trained model."""
    try:
        model = joblib.load(model_path)
        print("Model loaded successfully.")
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {model_path}.")

def evaluate_model(model, X, y):
    """Evaluate the model and print classification metrics."""
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    print("Model Evaluation:")
    print(f"Accuracy: {accuracy:.4f}")
    print(classification_report(y, y_pred, target_names=["Not Proxy", "Proxy"]))

if __name__ == "__main__":
    # Load model
    model_path = 'models/proxy_detection_rf_model.pkl'
    model = load_model(model_path)

    # Load and preprocess data
    data_path = 'data/preprocessed_data.csv'
    X_new, y_new = preprocess_data(data_path)

    # Evaluate the model
    evaluate_model(model, X_new, y_new)
