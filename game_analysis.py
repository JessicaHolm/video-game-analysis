import sys
from enum import Enum

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

WANTED_PLATFORMS = ["NES", "SNES", "N64", "GC", "Wii", "WiiU", "NS", "PS", "PS2", "PS3", "PS4", "XB", "X360", "XOne"]
PLATFORM_COLORS = ["blue", "green", "blue", "red", "blue", "blue", "green", "green", "red", "red", "red", "red", "red", "red"]

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

    def create_dataframe(self, col_name):
        col_dict = {}
        df = pd.DataFrame(self.games, columns=[col_name, "Total_Shipped"])
        col = df[col_name].unique()
        if col_name == "Critic_Score" or col_name == "User_Score":
            col = np.delete(col, np.where(np.isnan(col)))
        for value in col:
            sum = df.loc[df[col_name] == value, "Total_Shipped"].sum()
            if col_name == "Publisher" or col_name == "Platform":
                if col_name == "Platform":
                    if value in WANTED_PLATFORMS:
                        col_dict[value] = sum
                else:
                    if sum > 200:
                        col_dict[value] = sum
            else:
                col_dict[value] = sum
        self.simple_dicts.append(col_dict)

    def plot_dataframe(self, col_name, i):
        l = sorted(self.simple_dicts[i].items(), key=lambda e: e[1], reverse=True)
        keys = []
        values = []
        for (k,v) in l:
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
        plt.show()

    def create_and_plot_ratings(self):
        for col_name in ["Critic_Score", "User_Score"]:
            col_dict = {}
            df = pd.DataFrame(self.games, columns=[col_name, "Year"])
            col = df["Year"].unique()
            for value in col:
                sum = df.loc[df["Year"] == value, col_name].sum()
                count = df.loc[df["Year"] == value, col_name].count()
                average = sum / count
                col_dict[value] = average
            self.rating_dicts.append(col_dict)
            plt.plot(list(col_dict.keys()), list(col_dict.values()))
            plt.xlabel("Year")
            plt.ylabel(col_name)
            plt.show()

def main():
    games_file = sys.argv[1]

    a = Analysis(games_file)
    #for i, column in enumerate(Column):
        #print(column.value)
        #a.create_dataframe(column.value)
        #a.plot_dataframe(column.value, i)
    a.create_and_plot_ratings()


if __name__ == "__main__":
    main()