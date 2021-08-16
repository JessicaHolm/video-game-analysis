import sys
from enum import Enum

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

WANTED_PLATFORMS = ["PC", "NES", "SNES", "N64", "GC", "Wii", "WiiU", "NS", "PS", "PS2", "PS3", "PS4", "XB", "X360", "XOne"]
PLATFORM_COLORS = ["blue", "orange", "green", "blue", "red", "blue", "blue", "green", "green", "red", "red", "red", "red", "red", "red"]


class Column(Enum):
    YEAR = "Year"
    CRITIC = "Critic_Score"
    USER = "User_Score"
    PUBLISHER = "Publisher"
    PLATFORM = "Platform"


class Analysis(object):

    # Initialize the pandas DataFrames.
    def __init__(self, game_file):
        self.games = pd.read_csv(game_file)
        self.simple_dicts = []
        self.rating_dicts = []
        self.best_selling_dicts = []

    def create_dataframe(self, col_name):
        col_dict = {}
        df = pd.DataFrame(self.games, columns=[col_name, "Total_Shipped"])
        col = df[col_name].unique()
        sorted_col = sorted(col, key=lambda e: e, reverse=True)
        if col_name == "Critic_Score" or col_name == "User_Score":
            sorted_col = np.delete(sorted_col, np.where(np.isnan(sorted_col)))
        for value in sorted_col:
            sum = df.loc[df[col_name] == value, "Total_Shipped"].sum()
            if col_name == "Publisher" or col_name == "Platform":
                if col_name == "Platform":
                    if value in WANTED_PLATFORMS:
                        col_dict[value] = sum
                else:
                    if value == "Sony Computer Entertainment":
                        value = "Sony"
                    if sum > 200:
                        col_dict[value] = sum
            else:
                col_dict[value] = sum
        self.simple_dicts.append(col_dict)

    def plot_dataframe(self, col_name, i):
        l = sorted(self.simple_dicts[i].items(), key=lambda e: e[1], reverse=True)
        keys = []
        values = []
        for (k, v) in l:
            keys.append(k)
            values.append(v)
        if col_name == "Platform":
            plt.bar(keys, values, color=PLATFORM_COLORS)
        elif col_name == "Publisher":
            plt.barh(keys, values)
        else:
            plt.bar(keys, values)
        plt.xlabel(col_name)
        plt.ylabel("Total Game Sales")
        plt.title(col_name + " vs Total Game Sales")
        plt.show()

    def create_and_plot_ratings(self):
        for i, col_name in enumerate(["Critic_Score", "User_Score"]):
            col_dict = {}
            df = pd.DataFrame(self.games, columns=[col_name, "Year"])
            col = df["Year"].unique()
            sorted_col = sorted(col, key=lambda e: e)
            for value in sorted_col:
                if 2012 <= value <= 2018:
                    sum = df.loc[df["Year"] == value, col_name].sum()
                    count = df.loc[df["Year"] == value, col_name].count()
                    average = sum / count
                    col_dict[value] = average
            self.rating_dicts.append(col_dict)
            plt.plot(col_dict.keys(), col_dict.values())
            plt.ylim(6.0, 9.0)
            plt.xlabel("Year")
            plt.ylabel("Average " + col_name)
            plt.title("Average " + col_name + " of games in a given year")
            plt.show()

    def best_selling(self):
        for col_name in ["Critic_Score", "User_Score"]:
            col_dict = {}
            df = pd.DataFrame(self.games, columns=["Name", "Year", "Total_Shipped", "Critic_Score", "User_Score"])
            col = df["Year"].unique()
            sorted_col = sorted(col, key=lambda e: e, reverse=True)
            for value in sorted_col:
                if value >= 1985:
                    index = df.Year.eq(value).idxmax()
                    rating = df.at[index, col_name]
                    col_dict[value] = rating
            self.best_selling_dicts.append(col_dict)
            plt.plot(col_dict.keys(), col_dict.values())
            plt.xlabel("Year")
            plt.ylim(3.0, 10.0)
            plt.ylabel(col_name)
            plt.title("Ratings of the best selling game of each year")
            plt.show()


def main():
    games_file = sys.argv[1]

    a = Analysis(games_file)
    for i, column in enumerate(Column):
        a.create_dataframe(column.value)
        a.plot_dataframe(column.value, i)
    a.create_and_plot_ratings()
    a.best_selling()


if __name__ == "__main__":
    main()
