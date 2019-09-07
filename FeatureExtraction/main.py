import json
import sys
import numpy as np
import pandas as pd

# def generate_df_json_cols(df):
#     for col in df.columns:
#         series = df[col].copy()
#         df_col = pd.DataFrame(series.tolist()).dropna(axis=0)
#         df_col = df_col.astype({'id': 'int64'})
#         df_col = df_col.set_index('id')
#         df_col.to_csv(col + '.csv')
#         df[col] = df[col].apply(lambda x: x['id'] if 'id' in x else -1)
#     return df

def generate_df_json_cols(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x['name'] if 'name' in x else np.nan)
    return df

def generate_df_json_arr_cols(df):
    # For simplicity, for now we only take the first element of the array.
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x[0]['name'] if len(x) > 0 and 'name' in x[0] else np.nan)
    return df

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print('Usage: python main.py <path_to_json>')
        sys.exit(1)
    json_path = sys.argv[1]
    # json_path = "./KafkaStreamProcess/ProcessedDataSample/MovieDataStore.json"

    json_features = ['belongs_to_collection']
    json_arr_features = ['genres', 'production_companies', 'production_countries', 'spoken_languages']
    useless_features = ['original_title', 'homepage', 'poster_path', 'status', 'tagline']

    with open(json_path) as json_file:
        data = json.load(json_file)

    list_of_dict = [json.loads(data[movie_name]) for movie_name in data]

    df = pd.DataFrame(list_of_dict)
    df.set_index('tmdb_id')

    # drop the useless_features
    df = df.drop(useless_features, axis=1)

    df_json = generate_df_json_cols(df[json_features].copy())
    df = df.drop(json_features, axis=1)

    df_json_arr = generate_df_json_arr_cols(df[json_arr_features].copy())
    df = df.drop(json_arr_features, axis=1)

    result = pd.concat([df, df_json, df_json_arr], axis=1)
    result.to_csv('movie_data_clean.csv')
