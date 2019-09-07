#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Chenxi Li on 2019-09-07

import pandas as pd
rate_file = "data/RateData100000.json"
user_file = "data/UserDataStore.json"
movie_file = "data/MovieDataStore.json"

def extract_data_construct_csv():
    rate_data_store = extract_dict_from_file(rate_file)
    users = []
    movies = []
    scores = []
    for user_id in rate_data_store:
        for time_stamp in rate_data_store[user_id]:
            dict = rate_data_store[user_id][time_stamp]["basicInfo"]
            users.append(user_id)
            movies.append(dict['movieId'])
            scores.append(rate_data_store[user_id][time_stamp]['score'])

    dataframe = pd.DataFrame({'user_id': users, 'movie_id': movies, 'score': scores})
    dataframe.to_csv("rate100000.csv", index=False, sep=',')

def extract_dict_from_file(file_name):
    with open(file_name, "r") as file:
        return eval(file.read())

if __name__ == '__main__':
    extract_data_construct_csv()