
# src/preprocessing.py
import pandas as pd

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # target (used in training only)
    if 'G3' in df.columns:
        df['result'] = (df['G3'] >= 10).astype(int)

    
    if 'G3' in df.columns:
        df = df.drop(columns=['G3'])

    # one-hot encode categoricals
    df = pd.get_dummies(df, drop_first=True)

    return df

