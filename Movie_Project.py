import pandas as pd
import matplotlib.pyplot as plt
import ast

# Load the dataset
df = pd.read_csv("tmdb_5000_movies.csv")

# Extract the first genre from the JSON-like genres column
def get_first_genre(genre_str):
    try:
        genres = ast.literal_eval(genre_str)
        return genres[0]["name"] if genres else None
    except:
        return None

# Apply the function to create a clean genre column
df["primary_genre"] = df["genres"].apply(get_first_genre)

# Calculate average revenue by genre and plot top 10
genre_revenue = df.groupby("primary_genre")["revenue"].mean().sort_values(ascending=False).head(10)
print(genre_revenue)

genre_revenue.plot(kind="bar", color="steelblue")
plt.title("Average Revenue by Genre")
plt.xlabel("Genre")
plt.ylabel("Average Revenue ($)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# Remove movies with no budget data
df_clean = df[df["budget"] > 0]

# Plot budget vs rating to see if money affects quality
df_clean.plot(kind="scatter", x="budget", y="vote_average", color="steelblue")
plt.title("Budget vs Rating")
plt.xlabel("Budget ($)")
plt.ylabel("Average Rating")
plt.show()

# Extract year from release date
df["year"] = pd.to_datetime(df["release_date"]).dt.year

# Count movies per year and plot
year = df.groupby("year")["release_date"].count()
year.plot(kind="line", color="steelblue")
plt.title("Year Vs Movies")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

# Count movies per year and genre
df_yg = df.groupby(["year", "primary_genre"])["title"].count()

# Reshape and plot each genre as its own line
df_yg.unstack().plot(kind="line", figsize=(12, 6))
plt.title("Genre Popularity Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.legend(loc="upper left")
plt.show()