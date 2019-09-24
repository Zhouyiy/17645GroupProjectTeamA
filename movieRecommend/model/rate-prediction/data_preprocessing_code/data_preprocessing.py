#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Chenxi Li on 2019-09-24

prefix = "http://128.2.204.215:8080/user/"

import requests
import csv
import json

def read_csv(filename):
    data = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        counter = 0
        for row in csv_reader:
            if counter != 0:
                data.append(row)
            counter = counter + 1
    return data

def write_csv(rate_data, json_file_name, csv_file_name):
    with open(json_file_name) as json_file:
        data = json.load(json_file)
    row_datas = []
    for i in range(0, len(rate_data)):
        user_id = rate_data[i][0]
        movie_id = str(rate_data[i][1])
        rate = rate_data[i][2]
        item = data.get(str(movie_id))
        if item is not None:
            genres_data = json.loads(item)["genres"]
            genres = []
            if len(genres_data) > 0:
                for i in range(0, len(genres_data)):
                    genres.append(genres_data[i]["name"])
                age, gender, occupation = get_user_info(user_id)
                for genre in genres:
                    row_data = []
                    row_data.append(user_id)
                    row_data.append(age)
                    row_data.append(gender)
                    row_data.append(occupation)
                    row_data.append(genre)
                    row_data.append(rate)
                    row_datas.append(row_data)
    with open(csv_file_name, 'w') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_head = ["user_id", "age", "gender"]

        gernes = find_unique("training_data.csv")
        for genre in genres:
            csv_head.append(genre)
        csv_head.append("rate")

        csv_write.writerow(csv_head)
        for row_data in row_datas:
            csv_write.writerow(row_data)
    csv_file.close()
    json_file.close()

def write_final_data_file(input_file_name, output_file_name):
    data = read_csv(input_file_name)
    with open(output_file_name, 'w') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_head = ["user_id", "age", "male", "female"]
        genres = find_unique("training_data.csv")
        dict = get_index(genres)
        for genre in genres:
            csv_head.append(genre)
        csv_head.append("rate")
        csv_write.writerow(csv_head)
        for item in data:
            row_data = []
            row_data.append(item[0])
            row_data.append(item[1])
            if item[2] is "M":
                row_data.append(1)
                row_data.append(0)
            else:
                row_data.append(0)
                row_data.append(1)
            index = dict[item[4]]
            while len(row_data) < index:
                row_data.append(0)
            row_data.append(1)
            while len(row_data) < len(csv_head) - 1:
                row_data.append(0)
            row_data.append(item[5])
            csv_write.writerow(row_data)

def get_user_info(user_id):
    json = requests.get(prefix + str(user_id)).json()
    age = json['age']
    gender = json['gender']
    occupation = json['occupation']
    return age, gender, occupation

def find_unique(filename):
    data = read_csv(filename)
    dict = []
    for item in data:
        occupation = item[4]
        if occupation not in dict:
            dict.append(occupation)
    return dict

def get_index(genres):
    dict = {}
    counter = 4
    for genre in genres:
        dict[genre] = counter
        counter = counter + 1
    return dict


if __name__ == '__main__':
    # rate_data = read_csv("rate_data.csv")
    # write_csv(rate_data, "MovieDataStore400000.json", "training_data.csv")
    write_final_data_file("training_data.csv", "processed_data.csv")

