import os
import sys
import random
from time import time

import pandas as pd
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim

from model.KGAT import KGAT
from parser.parser_kgat import *
from utils.log_helper import *
from utils.metrics import *
from utils.model_helper import *
from data_loader.loader_kgat import DataLoaderKGAT


def evaluate_for_user(model, user_id, dataloader, device, top_k=10):
    """
    Evaluate the model for a single user and return the top_k predictions.
    """
    # model.eval()

    # Convert user_id and item_ids to tensors
    user_tensor = torch.LongTensor([user_id]).to(device)
    n_items = dataloader.n_items
    item_ids = torch.arange(n_items, dtype=torch.long).to(device)

    # Predict scores for all items for the given user
    with torch.no_grad():
        scores = model(user_tensor, item_ids, mode='predict')  # (1, n_items)

    scores = scores.cpu().numpy().flatten()

    # Exclude items the user has already interacted with
    train_user_dict = dataloader.train_user_dict
    interacted_items = set(train_user_dict.get(user_id, []))

    # Create a list of (item_id, score), filter out interacted items, and sort by score
    item_scores = [(item_id, score) for item_id, score in enumerate(scores) if item_id not in interacted_items]
    item_scores = sorted(item_scores, key=lambda x: x[1], reverse=True)

    # Get the top_k items
    top_items = item_scores[:top_k]
    return top_items


def predict_for_user(args, user_id):
    """
    Predict top 10 recommendations for a single user.
    """
    # GPU / CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load data
    data = DataLoaderKGAT(args, logging)

    # Load model
    model = KGAT(args, data.n_users, data.n_entities, data.n_relations)
    print("Im here!", args.pretrain_model_path)
    model = load_model(model, args.pretrain_model_path)
    model.to(device)

    # Predict top 10 items for the user
    top_k = 10
    top_items = evaluate_for_user(model, user_id, data, device, top_k)

    print(f"Top {top_k} recommendations for user {user_id}:")
    for rank, (item_id, score) in enumerate(top_items, start=1):
        print(f"{rank}: Item {item_id} with score {score}")

    return top_items




if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--seed', type=int, default=2019,
                        help='Random seed.')

    parser.add_argument('--data_name', nargs='?', default='amazon-book',
                        help='Choose a dataset from {yelp2018, last-fm, amazon-book}')
    parser.add_argument('--data_dir', nargs='?', default='datasets/',
                        help='Input data path.')

    parser.add_argument('--use_pretrain', type=int, default=1,
                        help='0: No pretrain, 1: Pretrain with the learned embeddings, 2: Pretrain with stored model.')
    parser.add_argument('--pretrain_embedding_dir', nargs='?', default='datasets/pretrain/',
                        help='Path of learned embeddings.')
    parser.add_argument('--pretrain_model_path', nargs='?', default='trained_model/model.pth',
                        help='Path of stored model.')

    parser.add_argument('--cf_batch_size', type=int, default=1024,
                        help='CF batch size.')
    parser.add_argument('--kg_batch_size', type=int, default=2048,
                        help='KG batch size.')
    parser.add_argument('--test_batch_size', type=int, default=10000,
                        help='Test batch size (the user number to test every batch).')

    parser.add_argument('--embed_dim', type=int, default=64,
                        help='User / entity Embedding size.')
    parser.add_argument('--relation_dim', type=int, default=64,
                        help='Relation Embedding size.')

    parser.add_argument('--laplacian_type', type=str, default='random-walk',
                        help='Specify the type of the adjacency (laplacian) matrix from {symmetric, random-walk}.')
    parser.add_argument('--aggregation_type', type=str, default='bi-interaction',
                        help='Specify the type of the aggregation layer from {gcn, graphsage, bi-interaction}.')
    parser.add_argument('--conv_dim_list', nargs='?', default='[64, 32, 16]',
                        help='Output sizes of every aggregation layer.')
    parser.add_argument('--mess_dropout', nargs='?', default='[0.1, 0.1, 0.1]',
                        help='Dropout probability w.r.t. message dropout for each deep layer. 0: no dropout.')

    parser.add_argument('--kg_l2loss_lambda', type=float, default=1e-5,
                        help='Lambda when calculating KG l2 loss.')
    parser.add_argument('--cf_l2loss_lambda', type=float, default=1e-5,
                        help='Lambda when calculating CF l2 loss.')

    parser.add_argument('--lr', type=float, default=0.0001,
                        help='Learning rate.')
    parser.add_argument('--n_epoch', type=int, default=1000,
                        help='Number of epoch.')
    parser.add_argument('--stopping_steps', type=int, default=10,
                        help='Number of epoch for early stopping')

    parser.add_argument('--cf_print_every', type=int, default=1,
                        help='Iter interval of printing CF loss.')
    parser.add_argument('--kg_print_every', type=int, default=1,
                        help='Iter interval of printing KG loss.')
    parser.add_argument('--evaluate_every', type=int, default=10,
                        help='Epoch interval of evaluating CF.')

    parser.add_argument('--Ks', nargs='?', default='[20, 40, 60, 80, 100]',
                        help='Calculate metric@K when evaluating.')
    parser.add_argument('--user_id', type=int, required=True, help="User ID to predict for")  # Thêm tham số user_id

    args = parser.parse_args()
    predict_for_user(args, user_id=args.user_id)


