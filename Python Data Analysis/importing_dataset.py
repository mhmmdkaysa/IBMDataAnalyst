# Installing pandas and numpy
mamba install pandas==1.3.3  -y
mamba install numpy=1.21.2 -y

# Import pandas library
import pandas as pd
import numpy as np

# Read data
from pyodide.http import pyfetch

async def download(url, filename):
    response = await pyfetch(url)
    if response.status == 200:
        with open(filename, "wb") as f:
            f.write(await response.bytes())

file_path='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv'

await download(file_path, "auto.csv")
file_name="auto.csv"

df = pd.read_csv(file_name)

filepath = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"
df = pd.read_csv(filepath, header=None)

# Show the first 5 rows of dataframe
df.head(5)

# Show the last 10 rows of dataframe
df.tail(10)

# Adding header to dataframe
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]

df.columns = headers
df.columns

# Replace the "?" symbol with NaN 
df1=df.replace('?',np.NaN)
df1

# Drop missing values in "price" column
df=df1.dropna(subset=["price"], axis=0)
df.head(20)

# Save dataset to local machine
df.to_csv("automobile.csv", index=False)

# Data types check
df.dtypes

# Checking data set info
df.info()

# Print statistical summary of dataframe
df.describe()

# Print statistical summary of all columns in dataframe
df.describe(include = "all")

# Select column in dataframe
df[['length', 'compression-ratio']]
