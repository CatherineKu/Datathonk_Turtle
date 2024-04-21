#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 20:04:31 2024

@author: chuhanku
"""
import pandas as pd

df_label = pd.read_csv('Book1.csv')
df = pd.read_csv("Atlanta_supply_dat.xlsx - UC_buildings.csv")

# Adding the second column of df_label into df
df['StageOfConstruction'] = df_label.iloc[:, 1]

df.fillna(0, inplace=True)

# Define a function to map size to quarters
def map_size_to_quarters(size):
    if size < 100000:
        return 2
    elif 100000 <= size < 300000:
        return 3
    elif 300000 <= size < 600000:
        return 4
    elif 600000 <= size < 1000000:
        return 5
    else:
        return 6

# Apply the function to create the new column
df['QuartedNeedToUse'] = df['Size_sf'].apply(map_size_to_quarters)


# Define the percentages corresponding to each stage of construction
percentages = {1: 0.0, 2: 0.25, 3: 0.35, 4: 0.65, 5: 0.925}

# Calculate the QuartedStillNeed based on StageOfConstruction and QuartedNeedToUse
df['QuartedStillNeed'] = df['QuartedNeedToUse'] - df['StageOfConstruction'].map(percentages) * df['QuartedNeedToUse']

df['QuartedStillNeed'].fillna(0, inplace=True)

df['RoundQuartedStillNeed'] = df['QuartedStillNeed'].apply(lambda x: int(x) + 1 if x % 1 > 0 else int(x))



# Print the DataFrame with the new column
# Viewing the updated df
#df.to_csv('output_file.csv', index=False)


# Count the number of occurrences of "ATLANT" in the "MarketCode" column
#atlant_count = df['MarketCode'].value_counts().get('ATLANT', 0)

# Print the count
#print("Number of occurrences of 'MarketCode' = 'ATLANT':", atlant_count)


# Create a new DataFrame with rows where 'MarketCode' is equal to 'ATLANT'


atlant_df = df[df['MarketCode'] == 'ATLANT']

non_atlant_df = df[df['MarketCode'] == 'FORTWO']


"""
atlant_df['y-factor'] = atlant_df['QuartedStillNeed']/atlant_df['QuartedNeedToUse']*atlant_df['Available_sf']

atlant_df['Ratio'] = atlant_df['Available_sf'] / atlant_df['QuartedNeedToUse']


atlant_df['2024.1'] = atlant_df['Ratio'] * 0 + atlant_df['y-factor']
atlant_df['2024.2'] = atlant_df['Ratio'] * 1 + atlant_df['y-factor']
atlant_df['2024.3'] = atlant_df['Ratio'] * 2 + atlant_df['y-factor']
atlant_df['2024.4'] = atlant_df['Ratio'] * 3 + atlant_df['y-factor']
atlant_df['2025.1'] = atlant_df['Ratio'] * 4 + atlant_df['y-factor']
atlant_df['2025.2'] = atlant_df['Ratio'] * 5 + atlant_df['y-factor']
"""




# Print the new DataFrame
atlant_df.to_csv('atlant_df.csv', index=False)


import math


# Initialize an empty list to store the new values for "NewEstimateTimeCompletion"
new_estimate_time_completion = []

# Iterate over the rows of the DataFrame
for index, row in non_atlant_df.iterrows():
    # Check if "YearQuarterGroundBroken" is NaN
    
       value = float('0.' + str(row['RoundQuartedStillNeed']))
   
     # Perform the addition
       estimate_quarter = 2024.1 + value
   
        # Round the result to 1 decimal place
       estimate_quarter = round(estimate_quarter, 1)
        #year, quarter = map(int, str(row['estimate_quarter']).split('.'))
        
        
        #new_estimate_time = 2024 + round(row['estimate_quarter'], 1)
        
       print(estimate_quarter)
        
       year, quarter = map(int, str(estimate_quarter).split('.'))
        # Adjust year if quarter is greater than 4
       if quarter > 4:
           year += 1
           quarter = quarter - 4
        
       new_estimate_time = float(f"{year}.{quarter}")
    
        
        # Append the new value to the list
       new_estimate_time_completion.append(new_estimate_time)

# Assign the list as a new column in atlant_df
non_atlant_df['NewEstimateTimeCompletion'] = new_estimate_time_completion

# Print the new DataFrame



#atlant_df.to_csv('atlant_df.csv', index=False)

# Initialize a dictionary to store the separated datasets
separated_datasets = {}



# Iterate over the rows of the DataFrame
for index, row in non_atlant_df.iterrows():
    # Get the value of NewEstimateTimeCompletion
    new_estimate_time = row['NewEstimateTimeCompletion']
    
    # If the value is not in the dictionary, create a new list
    if new_estimate_time not in separated_datasets:
        separated_datasets[new_estimate_time] = []
    
    # Append the row to the corresponding list in the dictionary
    separated_datasets[new_estimate_time].append(row)

# Convert the lists of rows into separate DataFrames
for value, rows in separated_datasets.items():
    separated_datasets[value] = pd.DataFrame(rows)



# Print the separated datasets
for value, dataset in separated_datasets.items():
    print(f"Dataset for NewEstimateTimeCompletion = {value}:")
    output_file = f"dataset_{value}.csv"
    dataset.to_csv(output_file, index=False)
    print("\n")



# Calculate the sum of "Available_sf" for each dataset
sum_available_sf = {}

for value, dataset in separated_datasets.items():
    sum_available_sf[value] = dataset['Available_sf'].sum()

# Print the sum of "Available_sf" for each dataset
for value, total in sum_available_sf.items():
    print(f"Sum of 'Available_sf' for NewEstimateTimeCompletion = {value}: {total}")


non_atlant_df.to_csv('non_atlant_df.csv', index=False)



'''

# Calculate the sum of each column separately
sum_2024_1 = atlant_df['2024.1'].sum()
sum_2024_2 = atlant_df['2024.2'].sum()
sum_2024_3 = atlant_df['2024.3'].sum()
sum_2024_4 = atlant_df['2024.4'].sum()
sum_2025_1 = atlant_df['2025.1'].sum()
sum_2025_2 = atlant_df['2025.2'].sum()

print("Sum of 2024.1 column:", sum_2024_1)
print("Sum of 2024.2 column:", sum_2024_2)
print("Sum of 2024.3 column:", sum_2024_3)
print("Sum of 2024.4 column:", sum_2024_4)
print("Sum of 2025.1 column:", sum_2025_1)
print("Sum of 2025.2 column:", sum_2025_2)

'''
