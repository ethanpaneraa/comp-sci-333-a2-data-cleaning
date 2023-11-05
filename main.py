import pandas as pd
import numpy as np

data_set = pd.read_csv("chicago-public-schools-high-school-progress-report-2013-2014.csv")
column_names = data_set.columns.tolist()

columns_to_drop = [
    'Phone Number', 'Website', 'Blue Ribbon Award', 'Historical Wards 2003-2015',
    'Boundaries - ZIP Codes', 'Community Areas', 'Census Tracts', 'Wards'
]

cleaned_data_set = data_set.drop(columns=columns_to_drop, errors='ignore')
cleaned_data_columns = cleaned_data_set.columns.tolist()

print(cleaned_data_columns)

#print(data_set.head())

#print(column_names)