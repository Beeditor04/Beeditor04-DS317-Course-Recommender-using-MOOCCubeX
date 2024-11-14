import torch
from torch import nn
from torch.nn import functional as F
import numpy as np
import scipy as sp

class HiddenLayer(nn.Module):

    def __init__(self, in_dim, out_dim, dropout):
        super(HiddenLayer, self).__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.dropout = dropout

        self.linear = nn.Linear(in_dim, out_dim)
        self.activation = nn.ReLU()
        self.message_dropout = nn.Dropout(dropout)

        nn.init.xavier_uniform_(self.linear.weight)


    def forward(self, x):
        out = self.linear(x)
        out = self.activation(out)
        out = self.message_dropout(out)
        return out


class NFM(nn.Module):

    def __init__(self, args,
                 n_users, n_items, n_entities, n_user_attr,
                 user_pre_embed=None, item_pre_embed=None):

        super(NFM, self).__init__()
        self.model_type = args.model_type
        self.use_pretrain = args.use_pretrain

        self.n_users = n_users
        self.n_items = n_items
        self.n_user_attr = n_user_attr
        self.n_entities = n_entities
        self.n_features = n_user_attr + n_entities

        self.embed_dim = args.embed_dim
        self.l2loss_lambda = args.l2loss_lambda

        self.hidden_dim_list = [args.embed_dim] + eval(args.hidden_dim_list)
        self.mess_dropout = eval(args.mess_dropout)
        self.n_layers = len(eval(args.hidden_dim_list))

        self.linear = nn.Linear(self.n_features, 1)
        nn.init.xavier_uniform_(self.linear.weight)

        if (self.use_pretrain == 1) and (user_pre_embed is not None) and (item_pre_embed is not None):
            other_entity_embed = nn.Parameter(torch.Tensor(self.n_entities - item_pre_embed.shape[0], self.embed_dim))
            nn.init.xavier_uniform_(other_entity_embed)
            user_entity_embed = torch.cat([user_pre_embed, item_pre_embed, other_entity_embed], dim=0)
            self.feature_embed = nn.Parameter(user_entity_embed)
        else:
            self.feature_embed = nn.Parameter(torch.Tensor(self.n_features, self.embed_dim))
            nn.init.xavier_uniform_(self.feature_embed)

        if self.model_type == 'fm':
            self.h = nn.Linear(self.embed_dim, 1, bias=False)
            with torch.no_grad():
                self.h.weight.copy_(torch.ones([1, self.embed_dim]))
            for param in self.h.parameters():
                param.requires_grad = False

        elif self.model_type == 'nfm':
            self.hidden_layers = nn.ModuleList()
            for idx in range(self.n_layers):
                self.hidden_layers.append(HiddenLayer(self.hidden_dim_list[idx], self.hidden_dim_list[idx + 1], self.mess_dropout[idx]))
            self.h = nn.Linear(self.hidden_dim_list[-1], 1, bias=False)
            nn.init.xavier_uniform_(self.h.weight)

    def convert_coo2tensor(self, coo):
        values = coo.data
        indices = np.vstack((coo.row, coo.col))

        i = torch.LongTensor(indices)
        v = torch.FloatTensor(values)
        shape = coo.shape
        return torch.sparse.FloatTensor(i, v, torch.Size(shape))
    
    # def calc_score(self, feature_values, device):
    #     """
    #     feature_values:  (batch_size, n_features), n_features = n_users + n_entities, torch.sparse.FloatTensor
    #     """
        
    #     batch_size, n_features = feature_values.shape
    #     embed_dim = self.feature_embed.shape[1]
        
    #     chunk_size = 1000  
    #     n_chunks = batch_size // chunk_size
        
    #     if batch_size % chunk_size != 0:
    #         n_chunks += 1
        
    #     z_list = []
        
    #     for i in range(n_chunks):
    #         start_idx = i * chunk_size
    #         end_idx = min((i + 1) * chunk_size, batch_size)
            
    #         chunk = feature_values[start_idx:end_idx, :]  # (chunk_size, n_features)
    #         chunk = self.convert_coo2tensor(chunk.tocoo()).to(device)
            
    #         # Bi-Interaction layer
    #         sum_square_embed = torch.mm(chunk, self.feature_embed).pow(2)          # (chunk_size, embed_dim)
    #         square_sum_embed = torch.mm(chunk.pow(2), self.feature_embed.pow(2))   # (chunk_size, embed_dim)
    #         z_chunk = 0.5 * (sum_square_embed - square_sum_embed)                  # (chunk_size, embed_dim)
            
    #         if self.model_type == 'nfm':
    #             # Equation (5)
    #             for layer in self.hidden_layers:
    #                 z_chunk = layer(z_chunk)  # (chunk_size, hidden_dim)
            
    #         z_list.append(z_chunk)
        
    #     # Ghép các phần nhỏ của z lại thành một ma trận
    #     z = torch.cat(z_list, dim=0)  # (batch_size, embed_dim)
        
    #     # Prediction layer
    #     y = self.h(z)  # (batch_size, 1)
        
    #     # Equation (2) / (7) / (8)
    #     feature_values = self.convert_coo2tensor(feature_values.tocoo()).to(device)
    #     y = self.linear(feature_values) + y  # (batch_size, 1)
        
    #     return y.squeeze()  # (batch_size)

    def calc_score(self, feature_values, device):
        """
        feature_values:  (batch_size, n_features), n_features = n_users + n_entities, torch.sparse.FloatTensor
        """
        # Bi-Interaction layer
        # Equation (4) / (3)
        feature_values = self.convert_coo2tensor(feature_values.tocoo()).to(device)
        sum_square_embed = torch.mm(feature_values, self.feature_embed).pow(2)           # (batch_size, embed_dim)
        square_sum_embed = torch.mm(feature_values.pow(2), self.feature_embed.pow(2))    # (batch_size, embed_dim)
        z = 0.5 * (sum_square_embed - square_sum_embed)                                  # (batch_size, embed_dim)

        if self.model_type == 'nfm':
            # Equation (5)
            for i, layer in enumerate(self.hidden_layers):
                z = layer(z)                                # (batch_size, hidden_dim)

        # Prediction layer
        # Equation (6)
        y = self.h(z)                                       # (batch_size, 1)
        # Equation (2) / (7) / (8)
        y = self.linear(feature_values) + y                 # (batch_size, 1)
        return y.squeeze()

    def calc_loss(self, pos_feature_values, neg_feature_values, device):
        """
        pos_feature_values:  (batch_size, n_features), torch.sparse.FloatTensor
        neg_feature_values:  (batch_size, n_features), torch.sparse.FloatTensor
        """
        pos_scores = self.calc_score(pos_feature_values, device)            # (batch_size)
        neg_scores = self.calc_score(neg_feature_values, device)            # (batch_size)

        loss = (-1.0) * torch.log(1e-10 + F.sigmoid(pos_scores - neg_scores))
        loss = torch.mean(loss)

        l2_loss = torch.norm(self.h.weight, 2).pow(2) / 2
        loss += self.l2loss_lambda * l2_loss
        return loss


    def forward(self, *input, is_train, device):
        if is_train:
            return self.calc_loss(*input, device)
        else:
            return self.calc_score(*input, device)


