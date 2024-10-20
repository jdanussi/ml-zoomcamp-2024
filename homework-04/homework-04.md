Question 1 = duration
Question 2 = 0.89
Question 3 = 0.265
Question 4 = 0.22
Question 5 = 0.006
Question 6 = 1


```python
roc_values = []

for feature in numerical:
        
    model = LogisticRegression(solver='liblinear', random_state=1)
    model.fit(df_train[feature].to_frame(), y_train)
    y_pred = model.predict_proba(df_val[feature].to_frame())
        
    roc_values.append((feature, roc_auc_score(y_val, y_pred[:,1])))
    
roc_values
```

