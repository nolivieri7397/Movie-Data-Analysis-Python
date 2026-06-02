import pandas as pd
from sqlalchemy import create_engine

# Load data
df = pd.read_csv("train.csv")

# Fix date columns
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

# Add useful columns
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Days to Ship"] = (df["Ship Date"] - df["Order Date"]).dt.days

# Drop duplicates
df = df.drop_duplicates()

# Check for missing values
print("Missing values:\n", df.isnull().sum())
print("Shape:", df.shape)

# Save to SQLite database
engine = create_engine("sqlite:///superstore.db")
df.to_sql("sales", engine, if_exists="replace", index=False)

print("Done! Data saved to superstore.db")