# train.py
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

# Tiny synthetic dataset: [monthly_spend, tenure_months, num_support_tickets]
X = np.array([
    [30, 2, 5],
    [80, 12, 0],
    [55, 6, 2],
    [20, 1, 9],
    [90, 24, 1],
    [45, 4, 3],
    [70, 10, 1],
    [25, 2, 8],
    [65, 8, 2],
    [35, 3, 6],
])
y = np.array([1,0,0,1,0,0,0,1,0,1])  # 1 = churn, 0 = stay

clf = LogisticRegression()
clf.fit(X, y)

with open("app/model.pkl", "wb") as f:
    pickle.dump(clf, f)

print("Wrote app/model.pkl")
