import pandas as pd
from sklearn.base import TransformerMixin


class ObservationCleaner(TransformerMixin):
    def __init__(self):
        pass

    def transform(self, df, *args):
        clean_df = df.copy()
        clean_df = clean_df.drop(['gender', 'earned dividends'], axis=1)
        clean_df['birth date'] = pd.to_datetime(clean_df['birth date']).astype(int)
        return clean_df

    def fit(self, *args):
        return self
