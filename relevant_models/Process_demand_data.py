import pandas as pd

def process_demand_data(input_csv, output_csv):
    """
    Leest de CSV in, voert berekeningen uit voor kolommen 2 en verder en slaat de resultaten op.
    
    Parameters:
    - input_csv: Pad naar het invoer-CSV-bestand.
    - output_csv: Pad waar het uitvoer-CSV-bestand wordt opgeslagen.
    """
    # 1. Lees de CSV in
    df = pd.read_csv(input_csv)

    # Houd non-numerieke kolommen (zoals 'Departure', 'Arrival') apart
    non_numeric_cols = ['Departure', 'Arrival']
    numeric_cols = [c for c in df.columns if c not in non_numeric_cols]

    # 2. Maak een kopie van de originele waarden
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
    df.to_csv(output_csv, index=False)

    # 5. Print om te checken
    print(f"The processed data has been saved to '{output_csv}'")
    print(df)

# Aanroep van de functie
process_demand_data('demand_data.csv', 'new_demand_data.csv')
