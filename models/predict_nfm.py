import sys
import random
import itertools
from time import time

import pandas as pd
from tqdm import tqdm
import scipy.sparse as sp
import torch.nn as nn
import torch.optim as optim
import torch.multiprocessing as mp

from model.NFM import NFM
from parser.parser_nfm import *
from utils.log_helper import *
from utils.metrics import *
from utils.model_helper import *
from data_loader.loader_nfm import DataLoaderNFM


def evaluate_batch(model, dataloader, user_ids, Ks):
    train_user_dict = dataloader.train_user_dict
    test_user_dict = dataloader.test_user_dict

    n_users = len(user_ids)
    n_items = dataloader.n_items
    item_ids = list(range(n_items))
    user_idx_map = dict(zip(user_ids, range(n_users)))

    feature_values = dataloader.generate_test_batch(user_ids)
    with torch.no_grad():
        scores = model(feature_values, is_train=False, device='cpu')              # (batch_size)

    rows = [user_idx_map[u] for u in np.repeat(user_ids, n_items).tolist()]
    cols = item_ids * n_users
    score_matrix = torch.Tensor(sp.coo_matrix((scores, (rows, cols)), shape=(n_users, n_items)).todense())

    user_ids = np.array(user_ids)
    item_ids = np.array(item_ids)
    metrics_dict = calc_metrics_at_k(score_matrix, train_user_dict, test_user_dict, user_ids, item_ids, Ks)

    score_matrix = score_matrix.numpy()
    return score_matrix, metrics_dict


def evaluate_mp(model, dataloader, Ks, num_processes, device):
    test_batch_size = dataloader.test_batch_size
    test_user_dict = dataloader.test_user_dict

    model.eval()
    model.to("cpu")

    user_ids = list(test_user_dict.keys())
    user_ids_batches = [user_ids[i: i + test_batch_size] for i in range(0, len(user_ids), test_batch_size)]

    pool = mp.Pool(num_processes)
    res = pool.starmap(evaluate_batch, [(model, dataloader, batch_user, Ks) for batch_user in user_ids_batches])
    pool.close()

    score_matrix = np.concatenate([r[0] for r in res], axis=0)
    metrics_dict = {k: {} for k in Ks}
    for k in Ks:
        for m in ['precision', 'recall', 'ndcg']:
            metrics_dict[k][m] = np.concatenate([r[1][k][m] for r in res]).mean()

    torch.cuda.empty_cache()
    model.to(device)
    return score_matrix, metrics_dict


def evaluate(model, dataloader, Ks, num_processes, device):
    test_batch_size = dataloader.test_batch_size
    train_user_dict = dataloader.train_user_dict
    test_user_dict = dataloader.test_user_dict

    model.eval()

    user_ids = list(test_user_dict.keys())
    user_ids_batches = [user_ids[i: i + test_batch_size] for i in range(0, len(user_ids), test_batch_size)]

    n_users = len(user_ids)
    n_items = dataloader.n_items
    item_ids = list(range(n_items))
    user_idx_map = dict(zip(user_ids, range(n_users)))

    cf_users = []
    cf_items = []
    cf_scores = []

    with tqdm(total=len(user_ids_batches), desc='Evaluating Iteration') as pbar:
        for batch_user in user_ids_batches:
            feature_values = dataloader.generate_test_batch(batch_user)
            # feature_values = feature_values.to(device)

            with torch.no_grad():
                batch_scores = model(feature_values, is_train=False, device=device)            # (batch_size)

            cf_users.extend(np.repeat(batch_user, n_items).tolist())
            cf_items.extend(item_ids * len(batch_user))
            cf_scores.append(batch_scores.cpu())
            pbar.update(1)

    rows = [user_idx_map[u] for u in cf_users]
    cols = cf_items
    cf_scores = torch.cat(cf_scores)
    cf_score_matrix = torch.Tensor(sp.coo_matrix((cf_scores, (rows, cols)), shape=(n_users, n_items)).todense())

    user_ids = np.array(user_ids)
    item_ids = np.array(item_ids)
    metrics_dict = calc_metrics_at_k(cf_score_matrix, train_user_dict, test_user_dict, user_ids, item_ids, Ks)

    cf_score_matrix = cf_score_matrix.numpy()
    for k in Ks:
        for m in ['precision', 'recall', 'ndcg']:
            metrics_dict[k][m] = metrics_dict[k][m].mean()
    return cf_score_matrix, metrics_dict


def predict(args):
    # GPU / CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # load data
    data = DataLoaderNFM(args, logging)

    # load model
    model = NFM(args, data.n_users, data.n_items, data.n_entities, data.n_user_attr)
    model = load_model(model, args.pretrain_model_path)
    model.to(device)

    # predict
    num_processes = args.test_cores
    if num_processes and num_processes > 1:
        evaluate_func = evaluate_mp
    else:
        evaluate_func = evaluate

    Ks = eval(args.Ks)

    cf_scores, metrics_dict = evaluate_func(model, data, Ks, num_processes, device)

    for k in Ks:
        print(f'*** CF Evaluation @{k} ***')
        print(f'Precision@{k}   : ', metrics_dict[k]['precision'])
        print(f'Recall@{k}      : ', metrics_dict[k]['recall'])
        print(f'NDCG@{k}        : ', metrics_dict[k]['ndcg'])

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    np.save(args.save_dir + 'cf_scores.npy', cf_scores)

if __name__ == '__main__':
    try:
        mp.set_start_method('spawn')
    except RuntimeError:
        pass

    args = parse_nfm_args()
    predict(args)
    # predict(args)