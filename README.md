<h1 align="center">Next Basket Recommendation</h1>
<p align="center"><b>A service for predicting a user's next purchase items</b></p>

## 1. Objective
The business objective is to increase the revenue of online stores and marketplaces by encouraging more repeat purchases from existing users.
This service leverages historical purchase data to *accurately predict* which items will be included in each user's next basket. The recommendations can increase basket diversity and value by suggesting new or forgotten items, and also improve user loyalty by simplifying the shopping process.

Predictions can be used for:
* 🖼 Contextual advertising
* 📧 Personalized mailings and promotions
* 🛍 Suggesting tailored product sets to speed up purchases
* 🛒 Recommending additional items before checkout

This problem is especially relevant given the growing importance of online shopping. In recent years, the ability to buy goods and groceries from home with just a few clicks has become more popular and essential than ever.

## 2. Problem Formulation
To align model evaluation with business goals, we use the following approach:
For each user-item pair (from all items previously purchased by the user), the algorithm predicts **1** or **0** depending on whether the user will buy this item in their next purchase.

This is a recommender system (RecSys) problem. The model outputs a set of products for each user, making it a ranking task. However, the order of recommendations is not important—only whether an item is included in the recommended basket.

The main evaluation metric is the **F1-score**, which balances precision and recall as their harmonic mean.

Note: Although the algorithm may use parameters like `top_k`, metrics such as _Precision@k_ or _Recall@k_ are not suitable here, since basket sizes vary and such metrics would reduce the problem to standard recommendations.

The ideal is to predict the user's next basket with perfect accuracy. The F1 threshold for model success can be set after initial A/B tests, which will help assess the model's economic impact (see section 6).

## 3. Data
The dataset comes from a [Kaggle competition](https://www.kaggle.com/c/sbermarket-internship-competition/).
It consists of three columns: *user_id*, *order_completed_at*, and *cart*.

  | user_id | order_completed_at   | cart
--|---------|---------------------|-----
0 | 2       | 2015-03-22 09:25:46 | 399
1 | 2       | 2015-03-22 09:25:46 | 14
2 | 2       | 2015-03-22 09:25:46 | 198
3 | 2       | 2015-03-22 09:25:46 | 88
4 | 2       | 2015-03-22 09:25:46 | 157

Here, *cart* is the ID of a product category, but the model can also work with data where this column contains specific product IDs.

The dataset contains **3,123,064** purchase records for **20,000** users, covering March 2015 to September 2020.

## 4. Solution Approaches
Several approaches were explored:
* Baseline models - `1. Baselines.ipynb`:
    * Recommend the most popular items overall
    * Recommend the most popular items for the user
    * Recommend the same items as in the user's last purchase
* Advanced aggregation of historical data (**best result**) - `3. TIFU KNN.ipynb`
* Classification using gradient boosting over decision trees - `4. ML Solution.ipynb`

See the corresponding notebooks for details on each approach.

Other approaches, such as the neural network-based DREAM method, were not implemented due to high computational requirements and, according to public research, lower performance compared to TIFU KNN. Other standard recommender system methods may also be considered.

Additionally, the `2. Apriori.ipynb` notebook explores association rule mining to find complementary products.

## 5. Final Model and Results
The best solution was a variation of the [TIFU KNN algorithm](https://arxiv.org/pdf/2006.00556.pdf):
1. Maximum (average over the last three purchases) F1-score: _bestScore_ = **0.39744**
2. Improvement over baseline models:
    - User last cart: **+0.069** (0.32841)
    - Top personal recs: **+0.0247** (0.37277) / **+0.073** (0.32415)
    - Top global recs: **+0.0220** (0.37593) / **+0.331** (0.36432)
3. Model validation was performed on the last three purchases of users. The standard deviation for these is **σ = 0.013**. A trend of decreasing F1 was observed when validating on earlier purchases, likely due to:
    - Less training data (earlier purchases mean less history)
    - Fewer items (some items only appear in later purchases)
    - Fewer users (the algorithm uses nearest neighbors for each user)
4. The final solution is an aggregation algorithm, so feature importance is not defined.
5. The model performs less well for new users with few or no purchases; for them, baseline models recommending popular items are preferable.
6. The model works best for users with a long history of similar purchases.
7. Model degradation: To maintain quality above _bestScore_ - σ, the model should be retrained after every two purchases for most users. The average interval between purchases is 2 days and 5 hours, so the model should ideally be retrained every ~2 days.

## 6. Economic Impact
It is difficult to assess the economic impact offline, since additional profit comes only from items the user would not have bought without the recommender system. We only have data on actual purchases.

Therefore, A/B testing is required wherever this service is used. During testing, the following metrics can be evaluated:
- Average order value
- Clicks
- Conversion rate

To further improve economic impact, consider product margin when deciding which items to recommend.

## 7. Demo

### Launch
```bash
git clone https://github.com/exsandebest/next-basket-recommendation.git
cd mts-teta-nbr/data
unzip users_as_vectors.zip
cd ../demo
streamlit run main.py
```

### Usage
1. Select the model and parameters
2. Enter the *user id* (1-19999)
3. Optionally, manually assemble another basket for this user to refine recommendations
4. Get recommendations