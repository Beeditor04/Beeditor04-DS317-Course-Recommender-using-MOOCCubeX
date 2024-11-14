import os
import sys
import random
from time import time

import pandas as pd
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim

from model.BPRMF import BPRMF
from parser.parser_bprmf import *
from utils.log_helper import *
from utils.metrics import *
from utils.model_helper import *
from data_loader.loader_bprmf import DataLoaderBPRMF


def evaluate(model, dataloader, Ks, device):
    test_batch_size = dataloader.test_batch_size
    train_user_dict = dataloader.train_user_dict
    test_user_dict = dataloader.test_user_dict

    model.eval()

    user_ids = list(test_user_dict.keys())
    user_ids_batches = [user_ids[i: i + test_batch_size] for i in range(0, len(user_ids), test_batch_size)]
    user_ids_batches = [torch.LongTensor(d) for d in user_ids_batches]

    n_items = dataloader.n_items
    item_ids = torch.arange(n_items, dtype=torch.long).to(device)

    cf_scores = []
    metric_names = ['precision', 'recall', 'ndcg']
    metrics_dict = {k: {m: [] for m in metric_names} for k in Ks}

    with tqdm(total=len(user_ids_batches), desc='Evaluating Iteration') as pbar:
        for batch_user_ids in user_ids_batches:
            batch_user_ids = batch_user_ids.to(device)

            with torch.no_grad():
                batch_scores = model(batch_user_ids, item_ids, is_train=False)       # (n_batch_users, n_items)

            batch_scores = batch_scores.cpu()
            batch_metrics = calc_metrics_at_k(batch_scores, train_user_dict, test_user_dict, batch_user_ids.cpu().numpy(), item_ids.cpu().numpy(), Ks)

            cf_scores.append(batch_scores.numpy())
            for k in Ks:
                for m in metric_names:
                    metrics_dict[k][m].append(batch_metrics[k][m])
            pbar.update(1)

    cf_scores = np.concatenate(cf_scores, axis=0)
    for k in Ks:
        for m in metric_names:
            metrics_dict[k][m] = np.concatenate(metrics_dict[k][m]).mean()
    return cf_scores, metrics_dict


def predict(args):
    # GPU / CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # load data
    data = DataLoaderBPRMF(args, logging)

    # load model
    model = BPRMF(args, data.n_users, data.n_items)
    model = load_model(model, args.pretrain_model_path)
    model.to(device)

    # predict
    Ks = eval(args.Ks)
    # k_min = min(Ks)
    # k_max = max(Ks)

    cf_scores, metrics_dict = evaluate(model, data, Ks, device)
    
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    np.save(args.save_dir + 'cf_scores.npy', cf_scores)
    
    for k in Ks:
        print(f'*** CF Evaluation @{k} ***')
        print(f'Precision@{k}   : ', metrics_dict[k]['precision'])
        print(f'Recall@{k}      : ', metrics_dict[k]['recall'])
        print(f'NDCG@{k}        : ', metrics_dict[k]['ndcg'])

if __name__ == '__main__':
    args = parse_bprmf_args()
    predict(args)


