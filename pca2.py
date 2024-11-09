import pandas as pd

data = pd.read_csv('homo_sapiens.csv')

# Fill Entry ID for empty values with the next non-empty ID until a new ID is encountered
data['Entry ID'] = data.groupby('Source Organism')['Entry ID'].fillna(method='bfill')

# Select Homo sapiens entries with exactly 3 accession codes
mask = (data['Source Organism'] == 'Homo sapiens') & (data['Accession Code(s)'].apply(lambda x: len(str(x).split(' ')) if pd.notna(x) else 0) == 3)

filtered_data = data[mask].copy()

def generate_combinations(row):
    codes = str(row['Accession Code(s)']).split(' ')
    combinations = [[codes[i], codes[(i + 1) % len(codes)]] for i in range(len(codes))]
    return combinations

# Print combinations in the specified pattern
for index, row in filtered_data.iterrows():
    entry_id = row['Entry ID']
    combinations = generate_combinations(row)
    if pd.notna(entry_id):
        print(f"{entry_id}: {combinations}")

filtered_data.to_csv('final_combinations.csv', index=False, columns=['Entry ID', 'Source Organism', 'Accession Code(s)'])
