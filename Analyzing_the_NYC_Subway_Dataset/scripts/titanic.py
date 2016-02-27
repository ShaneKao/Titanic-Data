import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import json

class titanic_analysis(object):
    def __init__(self):
        self.titanic_data_file = './data/titanic_data.csv' 
        self.titanic_data = pd.read_csv(self.titanic_data_file, header = False)
        self.titanic_data_cleaned = self.data_wrangling()              
    def data_wrangling(self):
        df = self.titanic_data.drop('Cabin', 1)[~self.titanic_data.Embarked.isnull()]
        df['Salutation'] = df.apply(lambda x: self.get_salutation(x['Name']), axis=1)
        med = df.groupby('Salutation')['Age'].transform('median')
        df['Age'] = df['Age'].fillna(med)
        return df
    def get_salutation(self, name):
        m = re.search(r'Miss\.|Mr\.|Mrs\.|Master\.|Rev\.', name)
        if m:
            salutation = m.group()
        else:
            salutation = 'other'
        return salutation
    def draw_pie_chart(self, gpby_col, filter_value):
        df = self.titanic_data.groupby([gpby_col, 'Survived'])[['Survived']].count()
        slices = df.iloc[df.index.get_level_values(gpby_col) == filter_value].Survived.tolist()
        activities = [0, 1]
        cols = ['r', 'g']
        plt.pie(slices, labels = activities, colors = cols, shadow = True, autopct = "%1.1f%%")
        plt.title(gpby_col + '=' + str(filter_value))
        plt.legend(('Not Survived','Survived'))
        plt.show()
        
    def get_treemap(self, x, y):
        df_count = self.titanic_data.groupby([x, y])[[y]].count()
        df_survival_rate = self.titanic_data.groupby([x, y, 'Survived'])[['Survived']].count()
        result = [['Location', 'Parent', 'Numbers of Passenger(size)', 'Survival Rate(color)'], [x + '&' + y, None, 0, 0]]
        for i in df_count.index.levels[0]:
            for j in df_count.index.levels[1]:      
                df_count_filter = df_count.iloc[df_count.index.get_level_values(df_count.index.names[0]) == i]
                df_count_filter = df_count_filter.iloc[df_count_filter.index.get_level_values(df_count.index.names[1]) == j]
                if df_count_filter[y].tolist():
                    df_survival_rate_filter = \
                    df_survival_rate.iloc[df_survival_rate.index.get_level_values(df_count.index.names[0]) == i]
                    df_survival_rate_filter =  \
                    df_survival_rate_filter.iloc[df_survival_rate_filter.index.get_level_values(df_count.index.names[1]) == j]
                    if df_survival_rate_filter.Survived.tolist():
                        df_survival_rate_filter = \
                        df_survival_rate_filter.iloc[df_survival_rate_filter.index.get_level_values('Survived') == 1]
                        if df_survival_rate_filter.Survived.tolist():
                            n_survived = df_survival_rate_filter.Survived.tolist()[0]
                        else:
                            n_survived = 0
                    result.append([df_count.index.names[0] + '=' + str(i) + '&' + df_count.index.names[1] + '=' + str(j),
                           df_count.index.names[0] + '&' + df_count.index.names[1],
                          int(df_count_filter[y].tolist()[0]), 
                           float(int(n_survived))/float(int(df_count_filter[y].tolist()[0]))])
     
        return json.dumps(result)    