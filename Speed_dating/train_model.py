import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier


def prepare_data(dataset):
    new_df = dataset.copy(deep=True)
    #binarize gender variable
    new_df['gender']=new_df['gender'].replace({new_df['gender'].unique()[0]:0,
                     new_df['gender'].unique()[1]:1})
    #transform target variable
    new_df['match'] =new_df['match'].apply(lambda x :x [2:-1]).astype(int)
    #dropping Nan Columns
    s =(new_df.isna().sum()/new_df.shape[0] > 0.08)
    columns_to_drop =s[s].index.values
    return new_df.select_dtypes(exclude=['object']).drop(columns = columns_to_drop).dropna()

if __name__ == '__main__':
    df = pd.read_csv("speeddating.csv")
    df_clean  =prepare_data(df)
    features_list = ["gender","age","age_o","attractive_o","sinsere_o","funny_o","intelligence_o",
     "funny_partner","attractive_partner","sincere_partner","intelligence_partner","shared_interests_important"]
    X = df_clean[features_list]
    y = df_clean['match']
    
    model = RandomForestClassifier(max_depth=10, min_samples_split=5, random_state=0)
    model.fit(X, y)
    joblib.dump(model, "model2.joblib")