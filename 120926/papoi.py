import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("Amazon- Movies and Films.csv")
    movie_counts_by_year = df.groupby("ReleaseYear")
    rating_by_year = df.groupby("ReleaseYear")["Rating"].mean()
    plt.plot(movie_counts_by_year.size(), rating_by_year["rating"])
    plt.show()

if __name__ == "__main__":
    main()