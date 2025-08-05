import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_bar_chart(df):
    """
    Generates a sorted horizontal bar chart of the AI Maturity Index
    for the top 10 countries. The chart is saved to the 'visuals' directory.
    """
    
    # Sort the data by AI Maturity Index for better readability
    df_sorted = df.sort_values('ai_maturity_index', ascending=True)

    # Use a smaller figure size for the top 10 countries
    plt.figure(figsize=(10, 8)) 
    
    # Create the horizontal bar chart
    plt.barh(df_sorted['country_iso'], df_sorted['ai_maturity_index'], color='skyblue')
    
    # Set labels and title
    plt.xlabel('AI Maturity Index Score')
    plt.ylabel('Country')
    plt.title('Top 10 AI Maturity Index by Country', fontsize=16)
    
    # Add data labels to the bars
    for index, value in enumerate(df_sorted['ai_maturity_index']):
        plt.text(value, index, f' {value:.2f}', va='center')
        
    # Adjusts plot to ensure everything fits without overlapping
    plt.tight_layout() 
    
    # Save the chart to the visuals folder
    plt.savefig('visuals/ai_maturity_top_10_bar_chart.png')
    
    # Close the plot to free up memory
    plt.close()

def create_heatmap(df):
    """
    Generates a heatmap to show the scores of different factors
    for the top 10 countries. The chart is saved to the 'visuals' directory.
    """
    
    # Select the relevant columns for the heatmap
    heatmap_df = df[['country_iso', 
                     'internet_users_pct_normalized', 
                     'gdp_per_capita_normalized',
                     'ai_use_cases_score', 
                     'regulation_score', 
                     'governance_frameworks_score']]
    
    # Rename columns for a cleaner display on the heatmap
    heatmap_df.columns = ['Country', 
                          'Internet Usage', 
                          'GDP per Capita', 
                          'AI Use Cases', 
                          'Regulation', 
                          'Governance']

    # Set the 'Country' column as the index for the heatmap
    heatmap_df = heatmap_df.set_index('Country')

    # Use a smaller figure size for the top 10 countries
    plt.figure(figsize=(12, 8)) 
    
    # Create the heatmap
    sns.heatmap(heatmap_df, annot=True, cmap='viridis', fmt=".2f", linewidths=.5, cbar_kws={'label': 'Score'})
    
    # Set title and labels
    plt.title('Top 10 AI Readiness Factors Heatmap', fontsize=16)
    plt.xlabel('Factors')
    plt.ylabel('Country')
    
    # Rotate x-axis labels to prevent overlap
    plt.xticks(rotation=45, ha='right') 
    
    # Ensure y-axis labels are horizontal
    plt.yticks(rotation=0) 
    
    # Adjust plot layout
    plt.tight_layout()
    
    # Save the chart to the visuals folder
    plt.savefig('visuals/ai_maturity_top_10_heatmap.png')
    
    # Close the plot
    plt.close()

if __name__ == "__main__":
    # Load the processed data
    try:
        df = pd.read_csv('data/processed_data/ai_maturity_index.csv')
    except FileNotFoundError:
        print("Error: 'ai_maturity_index.csv' not found. Please ensure 'process_data.py' has been run.")
        exit()

    # Data cleaning and type conversion
    df = df.dropna(subset=['country_iso'])
    df['country_iso'] = df['country_iso'].astype(str)
    
    # --- Filter the DataFrame to the top 10 countries ---
    df_top_10 = df.sort_values('ai_maturity_index', ascending=False).head(10)

    # Create the visualizations for the top 10 countries
    print("Generating bar chart for top 10 countries...")
    create_bar_chart(df_top_10)
    
    print("Generating heatmap for top 10 countries...")
    create_heatmap(df_top_10)
    
    print("Visualizations saved to the 'visuals/' directory.")