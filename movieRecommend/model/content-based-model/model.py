import numpy as np
import pyflann
import csv
import collections

"""
This is a Content Based Recommendation Model, it recommends similar movie to 
users from users' watch list.
"""

class ContentBasedModel:

    def __init__(self, recNum, splitRatio, MovieDatapath, UserDataPath):

        self.trainData = []
        self.movieId2Feature = {}
        self.movieFeatureIndex2MovieId = []

        self.user2MovieID = collections.defaultdict(dict)
        self.userRecBase = collections.defaultdict(dict)
        self.userRecTest = collections.defaultdict(dict)
        self.splitRatio = splitRatio

        self.model = None
        self.modelAppendix = None
        self.recNum = recNum

        self.MovieDatapath = MovieDatapath
        self.UserDataPath = UserDataPath

        self.loadMovieFeature()
        self.loadUserMovieData()
        self.trainTestSplit()

    """
    Train the model 
    """
    def train(self):
        flann_kdtree = pyflann.FLANN()
        params_kdtree = flann_kdtree.build_index\
            (np.array(self.trainData, dtype=float), algorithm='kdtree', trees=4)
        self.model = flann_kdtree
        self.modelAppendix = params_kdtree

    """
    Recommend movie given user id, return the similar movie from movie pool
    """
    def recommend(self, userId):
        if userId in self.userRecBase:
            recMovielist = []
            for movieId in self.user2MovieID[userId]:
                recMovielist += self.findSimMovie(movieId)
            return self.rankMovie(recMovielist)

    """
    Evalute the model on test dataset
    """
    def evaluate(self):
        hitnum = 0
        recommendedNum = 0
        actualInterestedNum = 0
        for userId in self.userRecTest:
            recList = self.recommend(userId)
            for movieId in recList:
                if movieId in self.userRecTest[userId]:
                    hitnum+=1
            recommendedNum += len(recList)
            actualInterestedNum += len(self.userRecTest[userId])
        print("Precision:", hitnum/(1.0*recommendedNum))
        print("Recall", hitnum/(1.0*actualInterestedNum))
        print("F score", 2 * hitnum/(1.0 * recommendedNum + actualInterestedNum))

    """
    Find the nearest K movie given movieId from the movie pool
    """
    def findSimMovie(self, movieId):
        if movieId in self.movieId2Feature:
            query_feature = np.array(self.movieId2Feature[movieId], dtype=float)
            resultsIndex, dists = self.model.nn_index(query_feature, self.recNum, checks=self.modelAppendix["checks"])
            result = []
            for idx in resultsIndex[0]:
                result.append(self.movieFeatureIndex2MovieId[idx])
            return result
        else:
            return []

    """
    Rank the merged recommended movie list and rerank the movie list 
    """
    def rankMovie(self, recMovieList):
        #Todo add rank movies by knn distance features
        return list(set(recMovieList))

    def loadMovieFeature(self):
        with open(self.MovieDatapath, newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=',')
            for row in file:
                fv = []
                for i in range(1, len(row)):
                    fv.append(float(row[i]))
                self.movieId2Feature[row[0]] = fv
                self.trainData.append(fv)
                self.movieFeatureIndex2MovieId.append(row[0])

    def loadUserMovieData(self):
        with open(self.UserDataPath, newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=',')
            for row in file:
                userId, movieId, rate = row[0], row[1], row[2]
                self.user2MovieID[userId][movieId] = rate

    def trainTestSplit(self):
        for userId, movieDict in self.user2MovieID.items():
            baseMovieNum = int(len(movieDict) * self.splitRatio + 0.9)
            if len(movieDict) == 1:
                continue
            for movieId, rating in movieDict.items():
                if baseMovieNum > 0:
                    self.userRecBase[userId][movieId] = rating
                else:
                    self.userRecTest[userId][movieId] = rating
                baseMovieNum -= 1

if __name__ == '__main__':
    MovieDatapath = "./moviefeature.csv"
    UserDataPath = "./usermovie.csv"
    RecommendationMovieNum = 2
    splitRatio = 0.5
    model = ContentBasedModel(RecommendationMovieNum, splitRatio, MovieDatapath, UserDataPath)
    model.train()
    model.evaluate()