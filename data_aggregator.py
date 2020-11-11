import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class Data_Aggregator:
    def __init__(self):
        self.score_array = []
        self.average_score_array = []
        self.df = pd.DataFrame(columns = ['Count', 'Score'])
        sns.scatterplot(x='Count', y='Score', data=self.df)
        plt.show()

    def add_score(self, score):
        self.score_array.append(score)
        if len(self.score_array) == 2:
            self.add_point_to_graph(self.score_array)
            self.score_array = []

    def add_point_to_graph(self, score_array):
        score_array = np.asarray(score_array)
        average_score = np.average(score_array)
        self.average_score_array.append(average_score)
        self.df = self.df.append({'Count': len(self.average_score_array), 'Score':average_score}, ignore_index = True)
        self.update_plot()

    def update_plot(self):
        # sns.scatterplot(x=pd.Series(np.arange(len(self.average_score_array))),y=pd.Series(self.average_score_array))
        sns.scatterplot(x = 'Count', y = 'Score', data = self.df)
        plt.show()

if __name__ == '__main__':
    arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    DA = Data_Aggregator()
    for i in arr:
        DA.add_score(i)