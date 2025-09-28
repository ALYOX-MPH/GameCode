def run_eda(df):
    # Géneros más comunes
    print("Géneros más populares:")
    print(df['Genre'].value_counts().head())

    # Plataformas más usadas
    print("\nPlataformas más comunes:")
    print(df['Platform'].value_counts().head())
