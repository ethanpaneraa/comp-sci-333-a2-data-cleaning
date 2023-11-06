import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

chicago_schools_data = pd.read_csv("chicago-public-schools-high-school-progress-report-2013-2014.csv")


column_names = chicago_schools_data.columns.tolist()

# columns to drop for the analysis (don't need them)
columns_to_drop = [
    'Phone Number', 'Website', 'Blue Ribbon Award', 'Historical Wards 2003-2015',
    'Boundaries - ZIP Codes', 'Community Areas', 'Census Tracts', 'Wards'
]

# Dropping the columns from the dataset
cleaned_data = chicago_schools_data.drop(columns=columns_to_drop, errors='ignore')

# Verify the drop by displaying the remaining columns
cleaned_data_columns = cleaned_data.columns.tolist()

# Calculate the number of missing values per column
missing_values = cleaned_data.isnull().sum()

# Display columns with missing values
missing_values_summary = missing_values[missing_values > 0].sort_values(ascending=False)

# List of crucial numeric columns for imputation
crucial_numeric_columns = [
    '4-Year Graduation Rate Percentage 2013',
    '5-Year Graduation Rate Percentage 2013',
    'College Enrollment Rate Percentage 2013',
    'College Persistence Rate Percentage 2013',
    'ACT Growth Percentile Grade 11',
    'Freshmen-on-Track Rate Percentage 2013',
    'Student Attendance Percentage 2013',
    'Teacher Attendance Percentage 2013'
]

# Impute missing values in the crucial numeric columns with the median
for column in crucial_numeric_columns:
    median_value = cleaned_data[column].median()
    cleaned_data[column] = cleaned_data[column].fillna(median_value)

# Check if the imputation worked by counting missing values in these columns again
imputed_missing_values = cleaned_data[crucial_numeric_columns].isnull().sum()

# Calculate the percentage of missing values for each column
missing_percentage = (cleaned_data.isnull().sum() / len(cleaned_data)) * 100

# Filter out columns with less than 50% missing values to consider for imputation
columns_to_consider = missing_percentage[(missing_percentage > 0) & (missing_percentage < 50)]

# Display the columns to consider for imputation along with their missing percentage
columns_to_consider.sort_values(ascending=False)

# Separating columns into numeric and categorical based on their content
numeric_columns_to_impute = columns_to_consider.index[columns_to_consider.index.str.contains('Percentage|Rate|Average|Attainment|Growth')]
categorical_columns_to_impute = columns_to_consider.index.difference(numeric_columns_to_impute)

# Imputing numeric columns with the median
for column in numeric_columns_to_impute:
    median_value = cleaned_data[column].median()
    cleaned_data[column] = cleaned_data[column].fillna(median_value)

# Imputing categorical columns with the mode or a placeholder
for column in categorical_columns_to_impute:
    mode_value = cleaned_data[column].mode()[0]  # mode() returns a series, so we take the first value
    cleaned_data[column] = cleaned_data[column].fillna(mode_value)

# Verify the imputation by counting missing values again
remaining_missing_values = cleaned_data.isnull().sum()
remaining_missing_values_summary = remaining_missing_values[remaining_missing_values > 0].sort_values(ascending=False)

# Insert placeholders for the remaining columns with missing values
# For numeric columns, we'll use -1 to indicate missing data
# For categorical columns like 'Zip Codes', we'll use "Not Available"

# Identify columns with numeric data
numeric_columns_with_missing = remaining_missing_values_summary[remaining_missing_values_summary.index.str.contains('Percentage|Rate|Average|Attainment|Growth|Length')].index

# Identify columns with categorical data
categorical_columns_with_missing = remaining_missing_values_summary.index.difference(numeric_columns_with_missing)

# Insert placeholders
for column in numeric_columns_with_missing:
    cleaned_data[column] = cleaned_data[column].fillna(-1)

for column in categorical_columns_with_missing:
    cleaned_data[column] = cleaned_data[column].fillna("Not Available")

# Check the final state of missing values
final_missing_values = cleaned_data.isnull().sum()
final_missing_values_summary = final_missing_values[final_missing_values > 0]

# save the cleaned data to a new csv file
cleaned_data.to_csv("cleaned_data.csv", index=False)