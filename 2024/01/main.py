
# %%
import pandas as pd

df = pd.read_csv('input.txt', sep=r'\s{3}', engine='python', header=None, names=['List1', 'List2'])

# %%
# sort each
df['List1'] = df['List1'].sort_values().values
df['List2'] = df['List2'].sort_values().values

# %%
# calc diff
df['Delta'] = (df['List1'] - df['List2']).abs()
total_distance = df['Delta'].sum()

print(total_distance) #2769675
# %%
# Part 2
df['CountInList2'] = df['List1'].apply(lambda x: (df['List2'] == x).sum())
df['SimilarityScore'] = df['List1'] * df['CountInList2']

# %%
plausability_check_df = df[df['CountInList2'] > 1]
print(plausability_check_df)

# %%
total_similarity_score = df['SimilarityScore'].sum()
print(total_similarity_score) #24643097
# %%
