#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Chenxi Li on 2019-09-07

import pandas as pd
rate_file = "data/RateData100000.json"
watch_file = "data/WatchData100000.json"

def extract_rate_dataframe():
    rate_data_store = extract_dict_from_file(rate_file)
    watch_data_store =extract_dict_from_file(watch_file)
    users = []
    movies = []
    scores = []
    block_size = []
    for user_id in rate_data_store:
        for movie_id in rate_data_store[user_id]:
            users.append(user_id)
            movies.append(movie_id)
            scores.append(rate_data_store[user_id][movie_id]['score'])
            block_size.append(-1)

    for user_id in watch_data_store:
        for movie_id in watch_data_store[user_id]:
            users.append(user_id)
            movies.append(movie_id)
            scores.append(-1)
            blocks = len(watch_data_store[user_id][movie_id])
            block_size.append(blocks)

    dataframe = pd.DataFrame({'user_id': users, 'movie_id': movies, 'score': scores, 'block_size': block_size})
    dataframe.to_csv("100000.csv", index=False, sep=',')

def extract_dict_from_file(file_name):
    with open(file_name, "r") as file:
        return eval(file.read())

if __name__ == '__main__':
    extract_rate_dataframe()