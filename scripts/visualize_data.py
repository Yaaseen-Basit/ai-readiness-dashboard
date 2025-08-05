import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure the visuals directory exists
if not os.path.exists('visuals'):
    os.makedirs('visuals')

def create_visuals(input_df_path):
    """
    Loads the processed data and generates visualizations.
    """
    print("Generating visualizations from processed data...")
    
    try:
        df = pd.read_csv(input_df_path)
    except FileNotFoundError:
        print(f"Error: The processed data file '{input_df_path}' was not found.")
        print("Please ensure you have run `src/process_data.py` successfully.")
        return

    # Sort the DataFrame by the index score for a clear presentation in both plots
    df_sorted = df.sort_values(by='ai_maturity_index', ascending=False)
    
    # --- 1. Bar Chart of the AI Maturity Index ---
    plt.figure(figsize=(12, 8))
    # Corrected `seaborn` call to address the FutureWarning
    sns.barplot(x='country_iso', y='ai_maturity_index', data=df_sorted, hue='country_iso', palette='viridis', legend=False)
    plt.title('AI Maturity Index by Country', fontsize=16)
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('AI Maturity Index Score', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the bar chart
    plt.savefig('visuals/ai_maturity_bar_chart.png')
    print("Bar chart saved to visuals/ai_maturity_bar_chart.png")
    
    # --- 2. Heatmap of Contributing Factors ---
    # Corrected the logic: we sort the original DataFrame first, then select columns
    heatmap_data = df_sorted.set_index('country_iso')[[
        'internet_users_pct_normalized',
        'gdp_per_capita_normalized',
        'ai_use_cases_score',
        'regulation_score',
        'governance_frameworks_score'
    ]]
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt=".2f", linewidths=.5)
    plt.title('AI Maturity Index Factors Heatmap', fontsize=16)
    plt.xlabel('Indicators', fontsize=12)
    plt.ylabel('Country', fontsize=12)
    plt.tight_layout()
    
    # Save the heatmap
    plt.savefig('visuals/ai_maturity_heatmap.png')
    print("Heatmap saved to visuals/ai_maturity_heatmap.png")
    
    plt.close('all') # Close all plots to free up memory

if __name__ == "__main__":
    create_visuals(
        input_df_path='data/processed_data/ai_maturity_index.csv'
    )