# This script merges the userid, movieid, rating csv file

import csv
import os

path = "."
userDict = {}
for filename in os.listdir(path):
    if filename.endswith(".kafka.csv"):
        with open(filename, newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=',')
            for row in file:
                userId, movieId, rate, blockSize = row[0], row[1], row[2], row[3]
                if userId not in userDict:
                    movieDict = {}
                    movieDict[movieId] = (rate, blockSize)
                    userDict[userId] = movieDict[movieId]
                else:
                    if movieId in userDict[userId]:
                        movieDict[movieId] = (movieDict[movieId][0] + rate, movieDict[movieId][1] + blockSize)



