import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    encoder = LabelEncoder()
    df['user_agent'] = encoder.fit_transform(df['user_agent'])
    X = df.drop(columns=['ip_address', 'is_proxy'])
    y = df['is_proxy']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

if __name__ == "__main__":
    X, y = preprocess_data('data/raw_data.csv')
    print(X[:5])
