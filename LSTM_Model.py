import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gc

from tqdm.auto import tqdm
import math
from sklearn.model_selection import KFold, StratifiedKFold, train_test_split, GridSearchCV
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import numpy as np

from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

tqdm.pandas()

rc = {
    "axes.facecolor": "#FFF9ED",
    "figure.facecolor": "#FFF9ED",
    "axes.edgecolor": "#000000",
    "grid.color": "#EBEBE7",
    "font.family": "serif",
    "axes.labelcolor": "#000000",
    "xtick.color": "#000000",
    "ytick.color": "#000000",
    "grid.alpha": 0.4
}

sns.set(rc=rc)

from colorama import Style, Fore
red = Style.BRIGHT + Fore.RED
blu = Style.BRIGHT + Fore.BLUE
mgt = Style.BRIGHT + Fore.MAGENTA
gld = Style.BRIGHT + Fore.YELLOW
res = Style.RESET_ALL

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
# load data
train = pd.read_csv("/kaggle/input/playground-series-s3e19/train.csv")
test = pd.read_csv("/kaggle/input/playground-series-s3e19/test.csv")

# summary table function
def summary(df):
    # Print the shape of the DataFrame
    print(f'data shape: {df.shape}')  
    # Create a summary DataFrame
    summ = pd.DataFrame(df.dtypes, columns=['data type'])
    # Calculate the number of missing values
    summ['#missing'] = df.isnull().sum().values 
    # Calculate the percentage of missing values
    summ['%missing'] = df.isnull().sum().values / len(df)* 100
    # Calculate the number of unique values
    summ['#unique'] = df.nunique().values
    # Create a descriptive DataFrame
    desc = pd.DataFrame(df.describe(include='all').transpose())
    # Add the minimum, maximum, and first three values to the summary DataFrame
    summ['min'] = desc['min'].values
    summ['max'] = desc['max'].values
    summ['first value'] = df.loc[0].values
    summ['second value'] = df.loc[1].values
    summ['third value'] = df.loc[2].values
    
    # Return the summary DataFrame
    return summ

summary(train)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df =train

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Aggregate num_sold by country and product
agg_df = df.groupby(['country', 'product']).num_sold.sum().reset_index()

# Visualize the results
plt.figure(figsize=(15, 8))

# Create a bar plot for each country
for country in agg_df['country'].unique():
    plt.bar(agg_df[agg_df['country'] == country]['product'], 
            agg_df[agg_df['country'] == country]['num_sold'], 
            alpha=0.5, 
            label=country)

plt.title('Total Num Sold by Country and Product')
plt.xlabel('Product')
plt.ylabel('Total Num Sold')
plt.xticks(rotation=45)
plt.legend()

plt.show()

# create graph by countries
countries = agg_df['country'].unique()

# Specify colors for each country
colors = ['b', 'g', 'r', 'c', 'm', 'y']

# Create a subplot for each country
fig, axs = plt.subplots(len(countries), 1, figsize=(15, 8*len(countries)))

for i, country in enumerate(countries):
    country_df = agg_df[agg_df['country'] == country]
    axs[i].bar(country_df['product'], country_df['num_sold'], alpha=0.5, color=colors[i], label=country)
    axs[i].set_title(f'Total Num Sold in {country} by Product')
    axs[i].set_xlabel('Product')
    axs[i].set_ylabel('Total Num Sold')
    axs[i].legend()
    axs[i].tick_params(axis='x', rotation=45) # Add this line to tilt x-axis labels
    
plt.tight_layout()
plt.show()

# Assuming 'date' is a string, convert it to datetime
df['date'] = pd.to_datetime(df['date'])

# Create a new DataFrame that aggregates num_sold by date, product, and country
time_df = df.groupby(['date', 'product', 'country'], as_index=False)['num_sold'].sum()

# Now, for each country, plot a line graph
countries = time_df['country'].unique()

fig, axs = plt.subplots(len(countries), 1, figsize=(15, 8*len(countries)))

for i, country in enumerate(countries):
    country_df = time_df[time_df['country'] == country]
    for product in country_df['product'].unique():
        product_df = country_df[country_df['product'] == product]
        axs[i].plot(product_df['date'], product_df['num_sold'], label=product)
    axs[i].set_title(f'Sales Over Time in {country} by Product')
    axs[i].set_xlabel('Date')
    axs[i].set_ylabel('Total Num Sold')
    axs[i].legend()

plt.tight_layout()
plt.show()

# Pivot the dataframe to have stores as columns and dates as index
df_pivot = df.pivot_table(index='date', columns='store', values='num_sold', aggfunc='sum')

# Plotting
plt.figure(figsize=(15,10))

for store in df_pivot.columns:
    plt.plot(df_pivot.index, df_pivot[store], label=store)

plt.title('Store-wise Product Sales Over Time', fontsize=15)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Products Sold', fontsize=12)
plt.legend()
plt.show()

# SMAPE function
def smape(A, F):
    return 100/len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))

# SMAPE Scorer
my_scorer = make_scorer(smape, greater_is_better=False)

# Convert 'date' to datetime
train['date'] = pd.to_datetime(train['date'])

# Create features from 'date'
train['year'] = train['date'].dt.year
train['month'] = train['date'].dt.month
train['day'] = train['date'].dt.day
train['dayofweek'] = train['date'].dt.dayofweek

# Creating moving average feature
train['moving_average'] = train['num_sold'].rolling(window=5).mean()

# Fill NA values caused by moving average
train = train.fillna(method='bfill')

# One-hot encoding
train = pd.get_dummies(train, columns=['country', 'store', 'product'])

# Define features X and target y
X = train.drop(['id', 'date', 'num_sold'], axis=1)
y = train[['num_sold']]

# Splitting data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
import lightgbm as lgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV

# Create a DMatrix for LightGBM
train_data = lgb.Dataset(X_train, label=y_train.values.ravel())

# Define parameters for grid search
param_search = {
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [20, 40],
    'boosting_type' : ['gbdt'],
    'objective' : ['regression'],
    'random_state' : [501], 
    'colsample_bytree' : [0.8, 0.1],
    'subsample' : [0.8, 1],
    'min_split_gain' : [0.01],
    'metric':['l1', 'l2'],
    'device': ['gpu'] # Enable GPU
}

# Cross-validation time series split
tscv = TimeSeriesSplit(n_splits=5)

# GridSearchCV
gsearch = GridSearchCV(lgb.LGBMRegressor(), param_grid=param_search, scoring=my_scorer, cv=tscv)
gsearch.fit(X_train, y_train.values.ravel())

# Best parameters
best_params = gsearch.best_params_
print("Best parameters: ", best_params)

# Train model with best parameters
model = lgb.LGBMRegressor(
    boosting_type=best_params['boosting_type'], 
    learning_rate=best_params['learning_rate'], 
    n_estimators=best_params['n_estimators'], 
    subsample=best_params['subsample'], 
    colsample_bytree=best_params['colsample_bytree'], 
    objective=best_params['objective'], 
    random_state=best_params['random_state'],
    device=best_params['device'])

model.fit(X_train, y_train.values.ravel())

# Make predictions
predictions = model.predict(X_test)

# Create subplots with 1 row and 2 columns
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Scatter plot of actual values vs predicted values
axes[0].scatter(y_test, predictions, color='blue', alpha=0.5)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', alpha=0.5, linewidth=2)
axes[0].set_xlabel('Actual Values')
axes[0].set_ylabel('Predicted Values')
axes[0].set_title('Scatter Plot: Predicted vs. Actual')
axes[0].legend(['Reference Line', 'Predicted vs. Actual'])

# Line plot of actual values and predicted values
axes[1].plot(y_test.values.ravel(), color='blue', alpha=0.5, label='Actual')
axes[1].plot(predictions, color='green', alpha=0.5, label='Predicted')
axes[1].set_title('Line Plot: Predicted vs. Actual')
axes[1].legend()

# Test set SMAPE
print("Test set SMAPE: ", smape(y_test.values.ravel(), predictions))

