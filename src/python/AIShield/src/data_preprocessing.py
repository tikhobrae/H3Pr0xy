import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def preprocess_data(file_path):
    df = pd.read_csv(file_path).copy()
    required_columns = ['user_agent', 'ip_address', 'is_proxy']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    df.dropna(subset=required_columns, inplace=True)
    encoder = LabelEncoder()
    df['user_agent'] = encoder.fit_transform(df['user_agent'])
    X = df.drop(columns=['ip_address', 'is_proxy'])
    y = df['is_proxy']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y

if __name__ == "__main__":
    X, y = preprocess_data('data/raw_data.csv')
    print("Sample of processed features:\n", X[:5])
    print("Sample of target values:\n", y[:5])
