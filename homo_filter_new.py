import pandas as pd
from itertools import combinations
data = pd.read_csv('homo_sapiens.csv')
data['Entry ID'] = data['Entry ID'].fillna(method='ffill')
data['Accession Code(s)'] = data['Accession Code(s)'].apply(lambda x: str(x).split(', ') if pd.notna(x) else [])
exploded_data = data.explode('Accession Code(s)')
exploded_data['Source Organism'] = exploded_data['Source Organism'].fillna('')
exploded_data = exploded_data.drop_duplicates(subset=['Entry ID', 'Accession Code(s)'], keep='first')
filtered = exploded_data[exploded_data['Source Organism'].str.contains('Homo sapiens', case=False)]
filtered_groups = filtered.groupby('Entry ID').filter(lambda x: x['Accession Code(s)'].count() == 3)
result = filtered_groups.groupby(['Entry ID', 'Source Organism'])['Accession Code(s)'].apply(lambda x: ','.join(str(code) for code in x.dropna())).reset_index()
result = result.groupby(['Entry ID'])['Source Organism', 'Accession Code(s)'].agg(lambda x: ','.join(x)).reset_index()
result['Source Organism']='Homo sapiens'
result.to_csv('filtered_accession_new.csv', index=False)
combinations_dict = {}
for index, row in result.iterrows():
    entry_id = row['Entry ID']
    accession_codes = set(row['Accession Code(s)'].split(','))
    code_combinations = list(combinations(accession_codes, 2))
    combinations_dict.setdefault(entry_id, []).extend(code_combinations)
combinations_df = pd.DataFrame(list(combinations_dict.items()), columns=['Entry ID', 'Accession Code Combinations'])
combinations_df.to_csv('accession_combinations_new.csv', index=False)