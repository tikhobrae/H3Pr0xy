import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from data_preprocessing import preprocess_data

def load_and_preprocess_data(file_path):
    """Load and preprocess data."""
    X, y = preprocess_data(file_path)
    return X, y

def train_and_evaluate_model(X, y, test_size=0.2, random_state=42):
    """Train the model and evaluate its performance on the test set."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    model.fit(X_train, y_train)
    print("Model training completed.")
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    print("Classification Report:\n", classification_report(y_test, y_pred, target_names=["Not Proxy", "Proxy"]))
    
    return model

def save_model(model, model_path):
    """Save the trained model to a file."""
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    data_path = 'data/raw_data.csv'
    model_path = 'models/proxy_detection_rf_model.pkl'
    X, y = load_and_preprocess_data(data_path)
    model = train_and_evaluate_model(X, y)
    save_model(model, model_path)
