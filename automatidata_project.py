import pandas as pd
import numpy as np

df = pd.read_csv('2017_Yellow_Taxi_Trip_Data.csv')
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

df.dropna(inplace=True)

pd.set_option('display.max_columns', None)

print("Shape:", df.shape)
print("\nData Types:")
print(df.dtypes)
print("\nNull Values (Missing Values):")
print(df.isnull().sum())
print("\nFirst 10 Rows:")
print(df.head(10))
print("\nDescribe:")
print(df.describe())