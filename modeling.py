# -*- coding: utf-8 -*-
"""Modeling

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cOvfXOVh3-U-DYZ0UcB7dW0It98kbjp7
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/IvanVC21/Tijuana-House-Prices/main/cleaned_data.csv'
df = pd.read_csv(url)

df.head(10)

df.columns

x = df[['bedrooms', 'bathrooms', 'parkingSpots', 'propertySize',
       'distance_SY (km)', 'distance_OT (km)']]
y = df[['price']]

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

x_test_df = pd.DataFrame(x_test)
x_test_df

from sklearn.preprocessing import StandardScaler
#sc = StandardScaler()
#x_train = sc.fit_transform(x_train)
#x_test = sc.transform(x_test)

from sklearn import metrics
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

ols = linear_model.LinearRegression()
ols.fit(x_train,y_train)
np.mean(cross_val_score(ols, x_train, y_train, cv = 5, scoring = "r2"))

model = linear_model.Lasso()
print("Lasso regression score: ", np.round(np.mean(cross_val_score(model, x_train, y_train, cv = 5, scoring = "r2")), 5))

from sklearn.model_selection import GridSearchCV

alphas = [0.01, 0.1,0.5,0.75,1]
model = linear_model.Lasso()
grid_lasso = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas), cv=5)
grid_lasso.fit(x_train, y_train)
print("Lasso regression best alpha value: ", grid_lasso.best_estimator_.alpha)
print("Lasso regression with hyperparameter tuning best score: ", np.round(grid_lasso.best_score_, 5))
print("Lasso regression improvement after hyperparameter tuning: {0}%".format(np.round((1 - ((np.round(np.mean(cross_val_score(model, x_train, y_train, cv = 5, scoring = "r2")), 5)) 
                                                                                             / np.round(grid_lasso.best_score_, 5))) * 100, 5)))

model = linear_model.Ridge()
print("Ridge regression score: ", np.round(np.mean(cross_val_score(model, x_train, y_train, cv = 5, scoring = "r2")), 5))

alphas = [int(x) for x in np.linspace(1, 10, num = 20)]
model = linear_model.Ridge()
grid_ridge = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas))
grid_ridge.fit(x_train, y_train)
print("Ridge regression best alpha value: ", grid_ridge.best_estimator_.alpha)
print("Ridge regression with hyperparameter tuning best score: ", np.round(grid_ridge.best_score_, 5))
print("Ridge regression improvement after hyperparameter tuning: {0}%".format(np.round((1 - ((np.round(np.mean(cross_val_score(model, x_train, y_train, cv = 5, scoring = "r2")), 5)) 
                                                                                             / np.round(grid_ridge.best_score_, 5))) * 100, 5)))

model = linear_model.ElasticNet()
print("Elastic Net regression score: ", np.round(np.mean(cross_val_score(model, x_train, y_train, cv = 5, scoring = "r2")), 5))

alphas = np.array([0.01, 0.02, 0.025, 0.05,0.1,0.5,1])
model = linear_model.ElasticNet()
grid_elastic = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas))
grid_elastic.fit(x_train, y_train)

print("Elastic Net regression best alpha value: ", grid_elastic.best_estimator_.alpha)
print("Elastic Net regression with hyperparameter tuning best score: ", np.round(grid_elastic.best_score_, 5))
print("Elastic Net regression improvement after hyperparameter tuning: {0}%".format(np.round((1 - ((np.round(np.mean(cross_val_score(model, x_train, y_train, cv = 5, scoring = "r2")), 5)) 
                                                                                             / np.round(grid_elastic.best_score_, 5))) * 100, 5)))

from sklearn.ensemble import RandomForestRegressor
rf_Model = RandomForestRegressor()
print("Random Forest regression score: ", np.round(np.mean(cross_val_score(rf_Model, x_train, y_train.values.ravel(), cv = 5, scoring = "r2")), 5))

param_grid = {'n_estimators': [int(x) for x in np.linspace(25, 75, num = 3)],
               'max_features': ['auto', 'sqrt'],
               'max_depth': [2, 4, 8],
               'min_samples_split': [2, 5,10],
               'min_samples_leaf': [1, 2, 4],
               'bootstrap': [True, False]}
print(param_grid)

from sklearn.ensemble import RandomForestRegressor
rf_Model = RandomForestRegressor()
rf_Grid = GridSearchCV(estimator = rf_Model, param_grid = param_grid, cv = 5, verbose=2, n_jobs = 4)
rf_Grid.fit(x_train, y_train.values.ravel())
print(rf_Grid.best_params_)
print("Random Forest regression with hyperparameter tuning best score: ", np.round(rf_Grid.best_score_, 5))
print("Random Forest regression improvement after hyperparameter tuning: {0}%".format(np.round((1 - ((np.round(np.mean(cross_val_score(rf_Model, x_train, y_train.values.ravel(), cv = 5, scoring = "r2")), 5)) 
                                                                                             / np.round(rf_Grid.best_score_, 5))) * 100, 5)))

from sklearn.ensemble import GradientBoostingRegressor
gbr = GradientBoostingRegressor()
print("Gradient Booster regression score: ", np.round(np.mean(cross_val_score(gbr, x_train, y_train.values.ravel(), cv = 5, scoring = "r2")), 5))

param_grid = {'n_estimators': [400, 500, 600],
               'learning_rate': [0.005, 0.01, 0.02],
               'max_depth': [1, 2, 4, 8],
               'subsample': [0.6, 0.8, 1]}
print(param_grid)

model = GradientBoostingRegressor()
grid_gbr = GridSearchCV(estimator = model, param_grid = param_grid, cv = 5, verbose=2, n_jobs = 4)
grid_gbr.fit(x_train, y_train.values.ravel())
print(grid_gbr.best_params_)
print("Gradient Booster regression with hyperparameter tuning best score: ", np.round(grid_gbr.best_score_, 5))
print("Gradient Booster regression improvement after hyperparameter tuning: {0}%".format(np.round((1 - ((np.round(np.mean(cross_val_score(gbr, x_train, y_train.values.ravel(), cv = 5, scoring = "r2")), 5)) 
                                                                                             / np.round(grid_gbr.best_score_, 5))) * 100, 5)))

import xgboost
xgb = xgboost.XGBRegressor()
np.mean(cross_val_score(xgb, x_train, y_train, cv = 5, scoring = "r2"))

param_grid = {'n_estimators': [int(x) for x in np.linspace(250, 500, num = 5)],
               'learning_rate': [0.01, 0.02, 0.03],
               'max_depth': [2, 4, 8],
               'colsample_bytree': [0.5,0.75, 1],
               'subsample': [0.6,0.8, 1]}
print(param_grid)

model = xgboost.XGBRegressor()
grid_xgb = GridSearchCV(estimator = model, param_grid = param_grid, cv = 5, verbose=2, n_jobs = 4)
grid_xgb.fit(x_train, y_train)
print(grid_xgb.best_params_)
print("XGBoost regression with hyperparameter tuning best score: ", np.round(grid_xgb.best_score_, 5))
print("XGBoost Forest regression improvement after hyperparameter tuning: {0}%".format(np.round((1 - ((np.round(np.mean(cross_val_score(xgb, x_train, y_train, cv = 5, scoring = "r2")), 5)) 
                                                                                             / np.round(grid_xgb.best_score_, 5))) * 100, 5)))

from sklearn.preprocessing import PolynomialFeatures
def create_polynomial_regression_model(degree):
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(x_train)
    poly = LinearRegression()
    return np.mean(cross_val_score(poly, X_poly, y_train, cv=5, scoring = "r2"))
cv_scores=[]
degrees =[2,3,4, 5]
for degree in degrees:
    cv_scores.append(create_polynomial_regression_model(degree))
    
print(max(cv_scores))

fig,ax=plt.subplots(figsize=(6,6))
ax.plot(degrees,cv_scores)
ax.set_xlabel('Degree',fontsize=20)
ax.set_ylabel('R2',fontsize=20)
ax.set_title('R2 VS Degree',fontsize=25)

poly_features = PolynomialFeatures(degree=2)
X_poly = poly_features.fit_transform(x_train)
poly = LinearRegression()
poly.fit(x_train, y_train)

ols_yhat = ols.predict(x_test)
lasso_yhat  = grid_lasso.best_estimator_.predict(x_test)
ridge_yhat = grid_ridge.best_estimator_.predict(x_test)
elastic_yhat = grid_elastic.best_estimator_.predict(x_test)
forest_yhat = rf_Grid.best_estimator_.predict(x_test)
gbr_yhat = grid_gbr.predict(x_test)
xgb_yhat = grid_xgb.predict(x_test)
poly_yhat = poly.predict(x_test)

from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

print("Ordinary Least Square accuracy: %.2f" % r2_score(y_test, ols_yhat) )
print("Lasso regression accuracy: %.2f" % r2_score(y_test, lasso_yhat) )
print("Ridge regression accuracy: %.2f" % r2_score(y_test, ridge_yhat) )
print("Elastic net regression accuracy: %.2f" % r2_score(y_test, elastic_yhat) )
print("Random forest regression accuracy: %.2f" % r2_score(y_test, forest_yhat) )
print("Gradient Booster regression accuracy: %.2f" % r2_score(y_test, gbr_yhat) )
print("XGBoost regression accuracy: %.2f" % r2_score(y_test, xgb_yhat) )
print("Polynomial regression accuracy: %.2f" % r2_score(y_test, poly_yhat) )

from sklearn.metrics import mean_squared_error


print("Ordinary Least Square accuracy: %.2f" % mean_squared_error(y_test, ols_yhat)) 
print("Lasso regression accuracy: %.2f" % mean_squared_error(y_test, lasso_yhat) )
print("Ridge regression accuracy: %.2f" % mean_squared_error(y_test, ridge_yhat) )
print("Elastic net regression accuracy: %.2f" % mean_squared_error(y_test, elastic_yhat) )
print("Random forest regression accuracy: %.2f" % mean_squared_error(y_test, forest_yhat) )
print("Gradient Booster regression accuracy: %.2f" % mean_squared_error(y_test, gbr_yhat) )
print("XGBoost regression accuracy: %.2f" % mean_squared_error(y_test, xgb_yhat) )
print("Polynomial regression accuracy: %.2f" % mean_squared_error(y_test, poly_yhat) )

xgb_ytest =  y_test.reset_index(drop=True)
xgb_ypred = pd.DataFrame(xgb_yhat)
dfs = [xgb_ytest, xgb_ypred ]
xgb_df = pd.concat(dfs, axis = 1)
xgb_df.rename(columns = {0:'predictions'}, inplace = True)
xgb_df

x_test_DF =pd.DataFrame(x_test)
x_test_DF

from sklearn.ensemble import StackingRegressor
estimators = [ ('gbr', GradientBoostingRegressor(learning_rate = 0.02, max_depth = 4, 
                                                 n_estimators = 600, subsample = 0.6)),
             ('rfr', RandomForestRegressor(bootstrap = 'False', max_depth = 8, max_features = 'sqrt', min_samples_leaf = 1, min_samples_split = 2, n_estimators = 75))]

stack = StackingRegressor(estimators = estimators, final_estimator = xgboost.XGBRegressor(colsample_bytree = 0.5, learning_rate = 0.02, max_depth =8, 
                                                                                          n_estimators = 312, subsample = 0.8) )
stack.fit(x_train, y_train.values.ravel())

stack_yhat = stack.predict(x_test)

print("Stack regression accuracy: %.2f" % r2_score(y_test, stack_yhat) )

# 'bedrooms', 'bathrooms', 'parkingSpots', 'propertySize',  'distance_SY (km)', 'distance_OT (km)'

x = [[2	, 1,	1	, 250	, 5.6,	6.07 ]]

#x = np.array([[2,1, 1, 750, 5.6, 6.07 ]])
#x = sc.fit_transform(x)
#inp = x.reshape(1, -1)
x = pd.DataFrame(x, columns = ['bedrooms', 'bathrooms', 'parkingSpots', 'propertySize',  'distance_SY (km)', 'distance_OT (km)'])
x

y_pred = grid_xgb.predict(x)
y_pred

import pickle

data = {"model": grid_xgb}
with open('saved_steps.pkl', 'wb') as file:
    pickle.dump(data, file)

with open('saved_steps.pkl', 'rb') as file:
    data = pickle.load(file)

regressor_loaded = data["model"]

y_pred = regressor_loaded.predict(x)
y_pred


