import csv

"""
This script filters the movieId that contains non-digit character
"""

path = "../../data/merged.kafka.csv"
outputPath = "./usermovie.csv"

result = []
with open(path, newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    for row in file:
        if not row[1].isdigit():
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
    #Todo later
    return