import pandas as pd
import os
import numpy as np

# Ensure the processed_data directory exists
if not os.path.exists('data/processed_data'):
    os.makedirs('data/processed_data')

def create_ai_maturity_index(output_df_path):
    """
    Loads raw data, processes it, and creates a weighted AI Maturity Index.
    """
    print("Creating AI Maturity Index from raw data...")
    
    # --- 1. Load Raw Data ---
    try:
        df_internet = pd.read_csv('data/raw_data/world_bank_internet_users.csv')
        df_gdp = pd.read_csv('data/raw_data/world_bank_gdp_per_capita.csv')
        # Note: We would also process the NLP results from the text files here.
        # For now, we'll use a mock DataFrame to show the scoring logic.
    except FileNotFoundError as e:
        print(f"Error: Required raw data file not found. Please ensure `data/collect_data.py` has run successfully. Error: {e}")
        return

    # --- 2. Data Cleaning and Pre-processing ---
    # We will use the most recent year's data for each country.
    df_internet = df_internet.sort_values('year', ascending=False).drop_duplicates(subset=['country_iso'], keep='first')
    df_gdp = df_gdp.sort_values('year', ascending=False).drop_duplicates(subset=['country_iso'], keep='first')

    # Rename columns for clarity
    df_internet = df_internet[['country_iso', 'value']].rename(columns={'value': 'internet_users_pct'})
    df_gdp = df_gdp[['country_iso', 'value']].rename(columns={'value': 'gdp_per_capita'})

    # --- 3. Data Integration (Merging) ---
    df_final = pd.merge(df_internet, df_gdp, on='country_iso', how='inner')

    # --- 4. Mock Data for NLP-Derived Scores ---
    # In a real project, these scores would come from your NLP analysis of the text files.
    # For now, we use a consistent mock score to demonstrate the final calculation.
    # We use a a random seed to make the numbers reproducible.
    np.random.seed(42)
    
    mock_data = {
        'country_iso': df_final['country_iso'].tolist(),
        'ai_use_cases_score': np.random.uniform(2.5, 5.0, size=len(df_final)).round(2),
        'regulation_score': np.random.uniform(2.0, 5.0, size=len(df_final)).round(2),
        'governance_frameworks_score': np.random.uniform(2.5, 5.0, size=len(df_final)).round(2),
        'talent_availability_score': np.random.uniform(2.0, 5.0, size=len(df_final)).round(2)
    }
    df_mock_scores = pd.DataFrame(mock_data)

    df_final = pd.merge(df_final, df_mock_scores, on='country_iso', how='inner')
    
    # --- 5. Data Normalization for a Consistent Scale ---
    # Since our indices are on different scales (e.g., % vs. dollars), we need to normalize them.
    # Let's use min-max scaling to bring everything to a 0-1 scale.
    for column in ['internet_users_pct', 'gdp_per_capita']:
        min_val = df_final[column].min()
        max_val = df_final[column].max()
        df_final[f'{column}_normalized'] = (df_final[column] - min_val) / (max_val - min_val)

    # --- 6. Calculate the Composite Index Score ---
    # Define the weights for each indicator. This is your core methodology.
    # You should justify these weights in your final report.
    weights = {
        'internet_users_pct_normalized': 0.15,
        'gdp_per_capita_normalized': 0.15,
        'ai_use_cases_score': 0.25,
        'regulation_score': 0.25,
        'governance_frameworks_score': 0.20
    }

    # Calculate the composite index score
    df_final['ai_maturity_index'] = (
        df_final['internet_users_pct_normalized'] * weights['internet_users_pct_normalized'] +
        df_final['gdp_per_capita_normalized'] * weights['gdp_per_capita_normalized'] +
        df_final['ai_use_cases_score'] * weights['ai_use_cases_score'] +
        df_final['regulation_score'] * weights['regulation_score'] +
        df_final['governance_frameworks_score'] * weights['governance_frameworks_score']
    )

    # Sort the results for easy viewing and save
    df_final = df_final.sort_values(by='ai_maturity_index', ascending=False)
    
    # Save the processed data
    df_final.to_csv(output_df_path, index=False)
    print(f"AI Maturity Index calculated and saved to {output_df_path}")
    print("\nFinal DataFrame Head:")
    print(df_final.head())


if __name__ == "__main__":
    create_ai_maturity_index(
        output_df_path='data/processed_data/ai_maturity_index.csv'
    )