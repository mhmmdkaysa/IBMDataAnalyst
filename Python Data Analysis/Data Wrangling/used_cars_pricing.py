# Import pandas, numpy, and matplotlib
mamba install pandas==1.3.3
mamba install numpy=1.21.2

import pandas as pd
import numpy as np
import matplotlib.pylab as plt



# Reading dasaset from the URL
from pyodide.http import pyfetch

async def download(url, filename):
    response = await pyfetch(url)
    if response.status == 200:
        with open(filename, "wb") as f:
            f.write(await response.bytes())

file_path="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"

await download(file_path, "usedcars.csv")
file_name="usedcars.csv"

# Create python list header
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]

df = pd.read_csv(file_name, names = headers)



# Replace missing value
df.replace("?", np.nan, inplace = True)

# Evaluating missing value using ".isnull()" or ".notnull()"
missing_data = df.isnull()
missing_data.head(5)

# Count missing value for each column
for column in missing_data.columns.values.tolist():
    print(column)
    print (missing_data[column].value_counts())
    print("")    

# Replace missing data in "normalized-losses", "stroke", "bore", "horsepower", "peak-rpm" columns with mean value
    # normalized-losses
    avg_norm_loss = df["normalized-losses"].astype("float").mean(axis=0)
    print("Average of normalized-losses:", avg_norm_loss)
    
    df["normalized-losses"].replace(np.nan, avg_norm_loss, inplace=True)
    
    # stroke
    avg_stroke = df['stroke'].astype('float').mean(axis=0)
    print("Average of stroke:", avg_stroke)
    
    df["stroke"].replace(np.nan, avg_stroke, inplace=True)
    
    # bore
    avg_bore=df['bore'].astype('float').mean(axis=0)
    print("Average of bore:", avg_bore)
    
    df["bore"].replace(np.nan, avg_bore, inplace=True)
    
    # horsepower
    avg_horsepower = df['horsepower'].astype('float').mean(axis=0)
    print("Average horsepower:", avg_horsepower)
    
    df['horsepower'].replace(np.nan, avg_horsepower, inplace=True)
    
    # peak-rpm
    avg_peakrpm=df['peak-rpm'].astype('float').mean(axis=0)
    print("Average peak rpm:", avg_peakrpm)
    
    df['peak-rpm'].replace(np.nan, avg_peakrpm, inplace=True)


# Replace missing data in "num-of-doors" column with mode value
df['num-of-doors'].value_counts()

df['num-of-doors'].value_counts().idxmax()

df["num-of-doors"].replace(np.nan, "four", inplace=True)

# Drop all row that do not have price data
df.dropna(subset=["price"], axis=0, inplace=True)

# reset index, because we droped two rows
df.reset_index(drop=True, inplace=True)



# Correct data format
df.dtypes()

# Convert data types to proper format
df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
df[["price"]] = df[["price"]].astype("float")
df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")

# Make sure all data already in proper format
df.dtypes()



# Data standardization
df.head()

# Convert mpg to L/100km by mathematical operation (235 divided by mpg)
df['city-L/100km'] = 235/df['city-mpg']

# Check the transformed data 
df.head(5)

# Convert mpg to L/100km in the column of "highway-mpg"
df["highway-mpg"] = 235/df["highway-mpg"]

# rename column name from "highway-mpg" to "highway-L/100km"
df.rename(columns={'"highway-mpg"':'highway-L/100km'}, inplace=True)

df.head()



# Data normalization
# Normalize those variables so their value ranges from 0 to 1
df['length'] = df['length']/df['length'].max()
df['width'] = df['width']/df['width'].max()
df['height'] = df['height']/df['height'].max()

df[['length','width','height']].head()



# Bining
df["horsepower"]=df["horsepower"].astype(int, copy=True)

# The histogram of horsepower to see the distribution of horsepower.
%matplotlib inline
import matplotlib as plt
from matplotlib import pyplot
plt.pyplot.hist(df["horsepower"])

plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")

# Find 3 bins of equal size bandwidth by using Numpy's linspace(start_value, end_value, numbers_generated)
bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]), 4)
bins

# Set group names
group_names = ['Low', 'Medium', 'High']

# Apply the function "cut" to determine what each value of df['horsepower'] belongs to.
df['horsepower-binned'] = pd.cut(df['horsepower'], bins, labels=group_names, include_lowest=True )
df[['horsepower','horsepower-binned']].head(20)

# See the number of each vehicle in each bin
df["horsepower-binned"].value_counts()

# Plot the distribution of each bin
%matplotlib inline
import matplotlib as plt
from matplotlib import pyplot
pyplot.bar(group_names, df["horsepower-binned"].value_counts())

plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")

# Make histogram visualization
%matplotlib inline
import matplotlib as plt
from matplotlib import pyplot

# draw historgram of attribute "horsepower" with bins = 3
plt.pyplot.hist(df["horsepower"], bins = 3)

plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")



# Indicator variable
df.columns

# Use the Panda method "get_dummies" to assign numerical values to different categories of fuel-type
dummy_variable_1 = pd.get_dummies(df["fuel-type"])
dummy_variable_1.head()

# Change the column names for clarity
dummy_variable_1.rename(columns={'gas':'fuel-type-gas', 'diesel':'fuel-type-diesel'}, inplace=True)
dummy_variable_1.head()

# Merge data frame "df" and "dummy_variable_1" 
df = pd.concat([df, dummy_variable_1], axis=1)

# Drop original column "fuel-type" from "df"
df.drop("fuel-type", axis = 1, inplace=True)

# Indicator variable for aspiration column
dummy_variable_2 = pd.get_dummies(df['aspiration'])
dummy_variable_2.rename(columns={'std':'aspiration-std', 'turbo':'aspiration-turbo'}, inplace=True)
dummy_variable_2.head()

# Merge data frame "df" and "dummy_variable_2" 
df = pd.concat([df, dummy_variable_2], axis=1)

# Drop original column "aspiration" from "df"
df.drop('aspiration', axis=1, inplace=True)



# Save the new CSV
df.to_csv('clean_df.csv')
