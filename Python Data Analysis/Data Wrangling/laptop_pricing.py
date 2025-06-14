# Importing required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# Download dataset into browser
from pyodide.http import pyfetch

async def download(url, filename):
    response = await pyfetch(url)
    if response.status == 200:
        with open(filename, "wb") as f:
            f.write(await response.bytes())

file_path= "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-Coursera/laptop_pricing_dataset_mod1.csv"

await download(file_path, "laptops.csv")
file_name="laptops.csv"

# Load dataframe into pandas.DataFrame
df = pd.read_csv(file_name, header=0)

# Verifying dataframe summary
print(df.info())

# Preview the dataset
df.head()

# Round "Screen_Size_cm" column values to nearest 2 decimal places
df[['Screen_Size_cm']] = np.round(df[['Screen_Size_cm']],2)
df.head()

# Find columns with missing data
missing_data = df.isnull()
missing_data.head(5)

for column in missing_data.columns.values.tolist():
    print(column)
    print (missing_data[column].value_counts())
    print("")    

# Replace missing values in "Weight_kg" column to mean value of all values in the column
avg_weight = df['Weight_kg'].astype('float').mean(axis=0)
avg_weight

df['Weight_kg'].replace(np.nan, avg_weight, inplace=True)

# Replace missing values in "Screen_Size_cm" column to most frequent value in the column
df['Screen_Size_cm'].value_counts()

df['Screen_Size_cm'].replace(np.nan, df['Screen_Size_cm'].value_counts().idxmax(), inplace=True)

# Fixing data types
df[['Screen_Size_cm', 'Weight_kg']] = df[['Screen_Size_cm', 'Weight_kg']].astype('float')
df.info()

# Data standardization
df['Screen_Size_cm'] = df['Screen_Size_cm']/2.54
df.rename(columns = {'Screen_Size_cm':'Screen_Size_inch'}, inplace=True)

df['Weight_kg'] = df['Weight_kg']*2.205
df.rename(columns = {'Weight_kg':'Weight_pounds'}, inplace=True)

# Data normalization
df['CPU_frequency'] = df['CPU_frequency']/df['CPU_frequency'].max()

# Bining value in "Price" column into 3 categories
bins = np.linspace(min(df["Price"]), max(df["Price"]), 4)

group_names = ['Low', 'Medium', 'High']

df['Price_bined'] = pd.cut(df['Price'], bins, labels=group_names, include_lowest=True )

df['Price_bined'].value_counts()

# Plot bar graph of the bins
%matplotlib inline
import matplotlib as plt
from matplotlib import pyplot
pyplot.bar(group_names, df["Price_bined"].value_counts())

plt.pyplot.xlabel("Price")
plt.pyplot.ylabel("Count")
plt.pyplot.title("Price bins")

# Convert "Screen" attribute into 2 numeric indicator variables
# Write your code below and press Shift+Enter to execute
dummy_var_1 = pd.get_dummies(df['Screen'])
dummy_var_1.head()

dummy_var_1.rename(columns={'Full HD': 'Screen_Full_HD', 'IPS Panel': 'Screen_IPS_Panel'}, inplace=True)
dummy_var_1.head()

df = pd.concat([df, dummy_var_1], axis=1)
df.head()

# Drop "Screen" column from dataframe
df.drop(['Screen'], axis=1, inplace=True)
df.head()

# Verify the changes that where made to the dataset
print(df.head())
