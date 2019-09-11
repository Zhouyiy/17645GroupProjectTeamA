from surprise import Dataset
from surprise import Reader
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate

from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise import KNNWithZScore
from surprise import SVD
from surprise import SVDpp
from surprise import NMF
from surprise import SlopeOne
from surprise import CoClustering

from collections import defaultdict
import os

"""
This class uses model-base model (SVD, MF ..) to recommend movies
"""
class ModelBasedModel:

    def __init__(self, modelName, dataPath):
        self.modelDict = {"KNNBasic":KNNBasic(), "KNNWithMeans":KNNWithMeans(),
             "KNNWithZScore": KNNWithZScore(), "SVD": SVD(),
             "SVDpp": SVDpp(), "NMF":NMF(),
             "SlopeOne": SlopeOne(), "CoClustering": CoClustering()}
        self.trainset = None
        self.testset = None
        self.data = None
        self.model = self.modelDict[modelName]
        self.loadData(os.path.expanduser(dataPath))

    def loadData(self, file_path):
        reader = Reader(line_format='user item rating', sep=',')
        self.data = Dataset.load_from_file(file_path, reader=reader)
        self.trainset, self.testset = train_test_split(self.data, test_size=.25)

    """
    This function predicts the RMSE of predicted movie rating
    """
    def EvaluateRMSEwithCrossValidation(self):
        algo = self.model
        cross_validate(algo, self.data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    """
    This function predicts the RMSE of predicted movie rating
    """
    def EvaluatePrecisionRecallwithRating(self):
        algo = self.model
        algo.fit(self.trainset)
        predictions = algo.test(self.testset)
        precisions, recalls = self.precision_recall_at_k(predictions, k=5, threshold=3)
        # Precision and recall can then be averaged over all users
        print(sum(prec for prec in precisions.values()) / len(precisions))
        print(sum(rec for rec in recalls.values()) / len(recalls))

    def EvaluatePrecisionRecallwithHitNum(self):
        algo = self.model
        algo.fit(self.trainset)
        predictions = algo.test(self.testset)
        precisions, recalls = self.precision_recall_by_hit_num(predictions, self.testset)
        # Precision and recall can then be averaged over all users
        print(sum(prec for prec in precisions.values()) / len(precisions))
        print(sum(rec for rec in recalls.values()) / len(recalls))

    """
    This function calculates the precision and recall
    It considers the recommended movie that has an actual rating that is higher than a threshold as relevent
    This function is from official suprise website https://surprise.readthedocs.io/en/stable/FAQ.html
    """
    def precision_recall_at_k(self, predictions, k, threshold):
        '''Return precision and recall at k metrics for each user.'''

        # First map the predictions to each user.
        user_est_true = defaultdict(list)
        for uid, _, true_r, est, _ in predictions:
            user_est_true[uid].append((est, true_r))
        precisions = dict()
        recalls = dict()
        for uid, user_ratings in user_est_true.items():
            # Sort user ratings by estimated value
            user_ratings.sort(key=lambda x: x[0], reverse=True)
            # Number of relevant items
            n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
            # Number of recommended items in top k
            n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])
            # Number of relevant and recommended items in top k
            n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                                  for (est, true_r) in user_ratings[:k])
            # Precision@K: Proportion of recommended items that are relevant
            precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 1
            # Recall@K: Proportion of relevant items that are recommended
            recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 1

        return precisions, recalls

    """
    This function calculates the precision and recall
    It considers the recommended movie that is in the user's watchlist as relevant
    This function is from official suprise website https://surprise.readthedocs.io/en/stable/FAQ.html
    """
    def precision_recall_by_hit_num(self, predictions, testset):
        # Todo Edit Later
        # First map the predictions to each user.
        user_est_true = defaultdict(list)
        for uid, movieId, true_r, est, _ in predictions:
            user_est_true[uid].append((est, true_r, movieId))

        precisions = dict()
        recalls = dict()
        user2TestMovieID = defaultdict(dict)
        user2RecMovieId = defaultdict(dict)

        for (userId, movieId, rate) in testset:
            user2TestMovieID[userId][movieId] = rate

        for uid, movieId, true_r, est, _ in predictions:
            user2RecMovieId[uid][movieId] = est

        hitNum = 0
        relevantMovieNum = 0
        recommenMovieNum = 0
        for uid in user2TestMovieID:
            testMovieList = user2TestMovieID[uid]
            recMovieList = user2RecMovieId[uid]
            relevantMovieNum += len(testMovieList)
            recommenMovieNum += len(recMovieList)
            hitNum = len(set(testMovieList).intersection(set(recMovieList)))

        precisions[0] = hitNum/ (1.0*recommenMovieNum)
        recalls[0] = hitNum/ (1.0*relevantMovieNum)

        return precisions, recalls

if __name__ == '__main__':
    UserDataPath = "./usermovie.csv"
    RecommendationMovieNum = 2
    splitRatio = 0.5
    model = ModelBasedModel("SVD", UserDataPath)
    #model.EvaluateRMSEwithCrossValidation()
    #model.EvaluatePrecisionRecallwithHitNum()
    model.EvaluatePrecisionRecallwithRating()
