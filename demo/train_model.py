import pandas as pd
import numpy as np
import pickle
import datetime as dt

from sklearn.neighbors import NearestNeighbors

import config as cfg


## вспомогательные функции

def duplicates_to_count(t):
    return t.groupby(['user_id', 'time'])['cart'].value_counts() \
                                                  .to_frame() \
                                                  .rename(columns={"cart":"count"}) \
                                                  .reset_index()
def user_cart_pivot_table(t):
    g = pd.pivot_table(t, columns="cart", index=["user_id", "time"], values="count", aggfunc=np.sum, fill_value=0)
    for cart in list(set(range(881)).difference(set(t["cart"].unique()))):
        g[cart] = 0
    return g

def get_user_one_cart_as_avg(users, r):
    user_as_avg_cart = [[]]
    cart = pd.Series(np.zeros(881), dtype=float)
    cur_weights = 0
    for j in range(len(users[0])):
        weight = r**(j)
        cart += pd.Series(users[0][j]) * weight
        cur_weights += weight
    if cur_weights == 0:
        cur_weights = 1
    cart /= cur_weights
    user_as_avg_cart[0] = cart.tolist()
    return user_as_avg_cart

def combine_with_neighbors_attenuation(user_cart, users_carts, neighbors, alpha, k_nearest):
    for j in range(1, k_nearest+1):
        user = user_cart[0]
        user += alpha**(j) * pd.Series(users_carts[neighbors[0][j]])
    return user


## Построение рекомендаций на основе TIFU KNN

def train_tifu(items_mapping, purchase_data, users_as_vectors, login, new_basket, model_params):
    
    purchase_data = pd.read_csv(cfg.purchase_data)
    purchase_data.rename(columns={"order_completed_at":"time"}, inplace=True)
    purchase_data["time"] = pd.to_datetime(purchase_data["time"], format="%Y-%m-%d %H:%M:%S")
    
    with open(cfg.users_as_vectors, 'rb') as data:
        users_as_vectors = pickle.load(data)
        
    # выбираем историю покупок конкретного клиента
    purchase_data = purchase_data[purchase_data['user_id'] == int(login)].copy()
        
    # добавляем новую корзину в историю покупок
    new_purc = []
    for i in list(items_mapping):
        if items_mapping[i]["title"] in new_basket:
            new_purc.append(i)
    if int(login) in range(20000):
        purchase_data = pd.concat([purchase_data, pd.DataFrame({'cart': new_purc,
                                                                'user_id': int(login),
                                                                'time': dt.datetime.today()})], ignore_index=True)
    else:
        purchase_data = pd.DataFrame({'cart': new_purc,
                                       'user_id': 20000,
                                       'time': dt.datetime.today()})
        
    if len(purchase_data) > 0:
        df = duplicates_to_count(purchase_data)
        df['cart'] = df['cart'].astype(int)
        main = user_cart_pivot_table(df)
        main = main.reindex(sorted(main.columns), axis=1).reset_index()
        main.sort_values('time', ascending=False, inplace=True)

        user_all_carts = [[]]
        main_array = main.to_numpy()
        for arr in main_array:
            user_all_carts[0].append(arr[2:])

        user_as_vector = get_user_one_cart_as_avg(user_all_carts, model_params['r'])

        # обновляем "средневзвешенную" корзину клиента
        if int(login) in range(20000):
            users_as_vectors[int(login)] = user_as_vector[0]
        else:
            users_as_vectors.append(user_as_vector[0])
    else:
        user_as_vector = [[0 for i in range(881)]]
        users_as_vectors.append(user_as_vector[0])
    
    # ищем ближайших соседей клиента
    model = NearestNeighbors()
    model.fit(users_as_vectors)
    neighbors = model.kneighbors(user_as_vector, n_neighbors=model_params['k_nearest']+1, return_distance=False)
    
    # комбинируем средневзвешенную корзину пользователя с корзинами его ближайших соседей
    user_as_final_vector = combine_with_neighbors_attenuation(user_as_vector,
                                                              users_as_vectors,
                                                              neighbors,
                                                              model_params['alpha'],
                                                              model_params['k_nearest'])
    # товарные рекомендации
    products = user_as_final_vector.sort_values(ascending=False).head(model_params['top_k']).index.tolist()
    products = [str(i) for i in products]
    recommendations = []
    for i in products:
        if i in list(items_mapping):
            recommendations.append(i)
            
    return recommendations


## Построение рекомендаций на основе топа популярных товаров

def train_popular(items_mapping, purchase_data, login, new_basket, model_params):
    
    purchase_data = pd.read_csv(cfg.purchase_data)
    purchase_data.rename(columns={"order_completed_at":"time"}, inplace=True)
    purchase_data["time"] = pd.to_datetime(purchase_data["time"], format="%Y-%m-%d %H:%M:%S")
    
    # добавляем новую корзину в историю покупок
    new_purc = []
    for i in list(items_mapping):
        if items_mapping[i]["title"] in new_basket:
            new_purc.append(i)    
    
    if len(new_purc) > 0:
        purchase_data = pd.concat([purchase_data, pd.DataFrame({'cart': new_purc,
                                                                'user_id': int(login),
                                                                'time': dt.datetime.today()})], ignore_index=True)  
    # товарные рекомендации
    products = purchase_data.groupby("cart")["user_id"].count().to_frame().reset_index() \
                   .sort_values("user_id", ascending=False).head(model_params['top_k'])["cart"].tolist()
    
    products = [str(i) for i in products]
    recommendations = []
    for i in products:
        if i in list(items_mapping):
            recommendations.append(i)
            
    return recommendations   