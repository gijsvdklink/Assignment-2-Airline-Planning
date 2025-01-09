import pandas as pd

# 1. Lees de CSV in
df = pd.read_csv('demand_data.csv')

# Houd non-numerieke kolommen (zoals 'Departure', 'Arrival') apart
non_numeric_cols = ['Departure', 'Arrival']
numeric_cols = [c for c in df.columns if c not in non_numeric_cols]

# 2. Maak een kopie van de originele waarden, zodat we bij de berekening
# altijd met "oude" waarden werken
df_orig = df.copy()

# 3. Voor i >= 2: nieuwe waarde = oude waarde + 0.2*(oude waarde van kolom i-1) + 0.2*(oude waarde van kolom i-2)
for i in range(2, len(numeric_cols)):
    col_i = numeric_cols[i]
    col_i_m1 = numeric_cols[i-1]  # i-1
    col_i_m2 = numeric_cols[i-2]  # i-2
    
    # Zorg dat we numeric uitvoeren op de kolommen
    df[col_i] = df_orig[col_i].astype(float) \
                + 0.2 * df_orig[col_i_m1].astype(float) \
                + 0.2 * df_orig[col_i_m2].astype(float)

# 4. Schrijf de nieuwe CSV weg
df.to_csv('new_demand_data.csv', index=False)

# 5. Print om te checken
print(df)
