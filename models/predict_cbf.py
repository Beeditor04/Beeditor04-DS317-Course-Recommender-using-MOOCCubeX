import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

def predict(user_batch, train_user_dict, courses_feats, weights=None):

    users_feats = {col: [] for col in courses_feats.keys()}

    for user in user_batch:
        used_courses = train_user_dict[user]
        for col, (enc, courses_feat) in courses_feats.items():
            users_feats[col].append(courses_feat[used_courses].mean(axis=0))

    if weights:
        assert len(weights) == len(courses_feats), 'weights must correspond to feat types'
    else:
        weights = [1] * len(courses_feats)

    for idx, col in enumerate(users_feats):
        users_feat = np.asarray(np.row_stack(users_feats[col]))
        courses_feat = courses_feats[col][1]
        weight = weights[idx]
        if idx == 0:
            cf_scores = weight * cosine_similarity(users_feat, courses_feat)
        else:
            cf_scores = cf_scores + weight * cosine_similarity(users_feat, courses_feat)

    return cf_scores


def eval(test_user_dict, train_user_dict, courses_feats, Ks, batch_size=500, weights=None, n_items=None):
    user_batches = list(range(len(test_user_dict)))
    user_batches = [user_batches[i: i+batch_size] for i in range(0, len(user_batches), batch_size)]

    metric_names = ['precision', 'recall', 'ndcg']
    metrics_dict = {k: {m: 0 for m in metric_names} for k in Ks}

    item_ids = list(range(n_items))

    with tqdm(total=len(user_batches), desc='Evaluating Iteration') as pbar:
        for user_batch in user_batches:
            batch_cf_scores = predict(user_batch, train_user_dict, courses_feats, weights)
            batch_metrics = calc_metrics_at_k(
                batch_cf_scores, train_user_dict, test_user_dict,
                user_batch, item_ids, Ks, num_negatives=100
            )

            for k in Ks:
                for m in metric_names:
                    metrics_dict[k][m] += batch_metrics[k][m].sum()

            pbar.update(1)

    for k in Ks:
        print(f'====== @{k} ======')
        for m in metric_names:
            metrics_dict[k][m] /= len(test_user_dict)
            print(f'{m}     : {metrics_dict[k][m]}')

    return metrics_dict
