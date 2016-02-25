from IPython.display import HTML
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
        return df
    def get_salutation(self, name):
        m = re.search(r'Miss\.|Mr\.|Mrs\.|Master\.|Rev\.|Dr\.', name)
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
        plt.legend('Not Survived','Survived')
        plt.show()