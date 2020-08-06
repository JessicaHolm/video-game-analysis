import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Analysis(object):

    # Initialize the pandas DataFrames.
    def __init__(self, game_file):
        self.games = pd.read_csv(game_file)
        self.years_dict = {}
        self.critic_dict = {}

    def create_dataframe(self, col_name):
        df = pd.DataFrame(self.games, columns=[col_name, "Total_Shipped"])
        col = df[col_name].unique()
        col = np.delete(col, np.where(np.isnan(col)))
        # print(col)
        for value in col:
            if col_name == "Year":
                self.years_dict[value] = df.loc[df["Year"] == value, "Total_Shipped"].sum()
                # print(self.years_dict)
            elif col_name == "Critic_Score":
                self.critic_dict[value] = df.loc[df["Critic_Score"] == value, "Total_Shipped"].sum()
                # print(self.critic_dict)

    def plot_dataframe(self, col_name):
        if col_name == "Year":
            plt.bar(list(self.years_dict.keys()), list(self.years_dict.values()))
            plt.xlabel("Year")
            plt.ylabel("Total Sales")
        elif col_name == "Critic_Score":
            plt.bar(list(self.critic_dict.keys()), list(self.critic_dict.values()))
            plt.xlabel("Critic Score")
            plt.ylabel("Total Sales")
        plt.show()

def main():
    games_file = sys.argv[1]

    a = Analysis(games_file)
    a.create_dataframe("Year")
    a.create_dataframe("Critic_Score")
    a.plot_dataframe("Year")
    a.plot_dataframe("Critic_Score")

if __name__ == "__main__":
    main()