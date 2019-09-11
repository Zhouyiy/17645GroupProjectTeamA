import csv

"""
This script filters the movieId that contains non-digit character
"""

path = "../../data/400000.kafka.csv"
outputPath = "./usermovie.csv"

result = []
with open(path, newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    for row in file:
        userId, movieId, rate, blockSize = row[0], row[1], row[2], row[3]
        if not str(rate).isdigit() or int(rate) < 0:
            continue
        result.append(row)

with open(outputPath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in result:
        writer.writerow(i)

"""
This function transform the blocksize into movie rating and output a userId, movieId, rateing csv
"""
def transformFromBlockSizetoRating():
    return