USER_ID="$1"

python src/models/predict_kgat.py \
    --data_dir "../../data/" \
    --data_name "" \
    --use_pretrain 2 \
    --pretrain_model_path "best_weight/model_epoch80.pth" \
    --n_epoch 6 \
    --cf_batch_size 1024 \
    --kg_batch_size 2048 \
    --test_batch_size 256 \
    --cf_print_every 500 \
    --kg_print_every 50 \
    --evaluate_every 2 \
    --Ks "[1, 5, 10]" \
    --user_id "$USER_ID" \
    --pretrain_embedding_dir ""
