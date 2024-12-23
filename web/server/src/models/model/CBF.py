import torch
from torch import nn
from torch.nn import functional as F
import numpy as np
from sklearn.metrics import roc_auc_score, log_loss, mean_squared_error

class CBF:
    def __init__(self):
        self.course_feats = None
        self.train_user_dict = None
    
    def precision_at_k_batch(hits, k):
        """
        calculate Precision@k
        hits: array, element is binary (0 / 1), 2-dim
        """
        res = hits[:, :k].mean(axis=1)
        return res

    def ndcg_at_k_batch(hits, k):
        """
        calculate NDCG@k
        hits: array, element is binary (0 / 1), 2-dim
        """
        hits_k = hits[:, :k]
        dcg = np.sum((2 ** hits_k - 1) / np.log2(np.arange(2, k + 2)), axis=1)

        sorted_hits_k = np.flip(np.sort(hits), axis=1)[:, :k]
        idcg = np.sum((2 ** sorted_hits_k - 1) / np.log2(np.arange(2, k + 2)), axis=1)

        idcg[idcg == 0] = np.inf
        ndcg = (dcg / idcg)
        return ndcg

    def recall_at_k_batch(hits, k):
        """
        calculate Recall@k
        hits: array, element is binary (0 / 1), 2-dim
        """
        res = (hits[:, :k].sum(axis=1) / hits.sum(axis=1))
        return res
    def calc_metrics_at_k(cf_scores, train_user_dict, test_user_dict, user_ids, item_ids, Ks, num_negatives=100):
        '''
        Calculate precision, recall, and NDCG at K for each user with negative sampling.
        Negative sampling selects 100 items that are neither the ground truth item nor in the user's train set.

        cf_scores: (n_users, n_items)
        '''

        binary_hit = []
        temp_cf_scores = []
        test_indices = []

        test_pos_item_binary = np.concatenate((
            np.ones((len(user_ids), 1)),
            np.zeros((len(user_ids), num_negatives))
        ), axis=1)

        for idx, user in enumerate(user_ids):
            # Ground truth items for the user
            test_item = set(test_user_dict[user])

            # Items in the training set to be excluded
            train_items = set(train_user_dict[user])

            # Negative samples: items not in the test items and not in the train items
            possible_negatives = [item for item in item_ids if item not in train_items and item not in test_item]
            negative_samples = np.random.choice(possible_negatives, num_negatives, replace=False)

            # Selected items for testing: ground truth + negative samples
            test_set = list(test_item) + list(negative_samples)
            # test_indices.append(test_set)

            # Get the corresponding scores of these items from the cf_scores matrix
            temp_cf_scores.append(cf_scores[idx][test_set].tolist())

        try:
            _, rank_indices = torch.sort(torch.LongTensor(temp_cf_scores).cuda(), descending=True)    # try to speed up the sorting process
        except:
            _, rank_indices = torch.sort(torch.LongTensor(temp_cf_scores), descending=True)

        rank_indices = rank_indices.cpu()

        # binary_hit = [] # shape (n_users, num_negatives+1)
        # test_indices = np.asarray(test_indices)

        for i in range(len(user_ids)):
            binary_hit.append(test_pos_item_binary[i][rank_indices[i]])
        binary_hit = np.array(binary_hit, dtype=np.float32)

        metrics_dict = {}
        for k in Ks:
            metrics_dict[k] = {}
            metrics_dict[k]['precision'] = precision_at_k_batch(binary_hit, k)
            metrics_dict[k]['recall']    = recall_at_k_batch(binary_hit, k)
            metrics_dict[k]['ndcg']      = ndcg_at_k_batch(binary_hit, k)

        return metrics_dict   