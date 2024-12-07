import numpy as np
import polars as pl
import pandas as pd
import os
import gc
from tqdm import tqdm

from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import coo_matrix, hstack, csr_matrix, vstack
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline

import torch
from sklearn.metrics import roc_auc_score, log_loss, mean_squared_error

class Recommender
    def __init__(self):
        self.course_feats = None
        self.train_user_dict = None

    def fit(self, courses_feats, train_user_dict):
        self.courses_feats = courses_feats
        self.train_user_dict = train_user_dict
        self.n_users = len(train_user_dict)
        for col, (enc, feats) in self.courses_feats.items():
            self.n_items = feats.shape[0]
            break

    def predict(self, user_batch, weights=None):
        # Get features of users
        users_feats = {col: [] for col in self.courses_feats.keys()}

        for user in user_batch:
            used_courses = self.train_user_dict[user]
            for col, (enc, courses_feat) in self.courses_feats.items():
                users_feats[col].append(courses_feat[used_courses].mean(axis=0))

        # Calculate cf_scores
        if weights:
            assert len(weights) == len(self.courses_feats), 'weights must correspond to feat types'
        else:
            weights = [1] * len(self.courses_feats)

        for idx, col in enumerate(users_feats):
            users_feat = np.asarray(np.row_stack(users_feats[col]))
            courses_feat = self.courses_feats[col][1]
            weight = weights[idx]
            if idx == 0:
                cf_scores = weight * cosine_similarity(users_feat, courses_feat)
            else:
                cf_scores = cf_scores + weight * cosine_similarity(users_feat, courses_feat)

        return cf_scores

    def recommend(self, user_batch, topk=10, weights=None):
        cf_scores = self.predict(user_batch, weights)

        for idx, user in enumerate(user_batch):
            cf_scores[idx][self.train_user_dict[user]] = -10

        ranked_courses = np.argsort(cf_scores)[:, ::-1]
        return ranked_courses[:topk]

    def eval(self, test_user_dict, Ks, batch_size=500, weights=None):
        # Predict
        user_batches = list(range(len(test_user_dict)))
        user_batches = [user_batches[i: i+batch_size] for i in range(0, len(user_batches), batch_size)]

        metric_names = ['precision', 'recall', 'ndcg']
        metrics_dict = {k: {m: 0 for m in metric_names} for k in Ks}

        item_ids = list(range(self.n_items))

        with tqdm(total=len(user_batches), desc='Evaluating Iteration') as pbar:
            for user_batch in user_batches:
                batch_cf_scores = self.predict(user_batch)
                batch_metrics = calc_metrics_at_k(
                    batch_cf_scores, self.train_user_dict, test_user_dict,
                    user_batch, item_ids, Ks, num_negatives=100
                )

                for k in Ks:
                    for m in metric_names:
                        metrics_dict[k][m] += batch_metrics[k][m].sum()

                pbar.update(1)

        # Cal mean
        for k in Ks:
            print(f'====== @{k} ======')
            for m in metric_names:
                metrics_dict[k][m] /= len(test_user_dict)
                print(f'{m}     : {metrics_dict[k][m]}')

        return metrics_dict