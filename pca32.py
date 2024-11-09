import pandas as pd
from itertools import combinations

# Original code to read and preprocess the data
df = pd.read_csv('homo_sapiens.csv').fillna(method='ffill', axis=0)
homo_df = df[df['Source Organism'].str.contains('Homo sapiens', na=False)]

# Combine Accession codes for the same Entry IDs into lists
combined_df = homo_df.groupby('Entry ID', as_index=False).agg({
    'Source Organism': lambda x: 'Homo sapiens',
    'Accession Code(s)': lambda x: x.dropna().unique().tolist()
})

# Task 1: Obtain entry ids with only three accession codes of Homo sapiens
filtered_df_task1 = combined_df[combined_df['Accession Code(s)'].apply(lambda x: len(x) == 3)]

# Write Task 1 result to a separate CSV file
filtered_df_task1.to_csv('filtered_data_task1.csv', index=False)

# Task 2: Generate accession code combinations of two for each entry id
combinations_data = []
for entry_id, accession_codes in zip(filtered_df_task1['Entry ID'], filtered_df_task1['Accession Code(s)']):
    combinations_data.extend({'Entry_ID': entry_id, 'Source_Organism': 'Homo sapiens', 'Accession_Code': comb} for comb in combinations(accession_codes, 2))

# Create a DataFrame from the list of dictionaries for Task 2
combinations_df_task2 = pd.DataFrame(combinations_data)

# Write Task 2 result to a separate CSV file
combinations_df_task2.to_csv('combinations_data_task2.csv', index=False)

# Display the final result for Task 2
print(combinations_df_task2)