import pandas as pd
import plotly.express as px

def create_choropleth_map(df):
    """
    Generates an interactive choropleth map of the AI Maturity Index.
    """
    fig = px.choropleth(df, 
                        locations="country_iso",
                        color="ai_maturity_index",
                        hover_name="country_name",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title="AI Maturity Index by Country")
    
    fig.write_html("visuals/ai_maturity_choropleth_map.html")
    print("Interactive choropleth map saved to visuals/ai_maturity_choropleth_map.html")

def create_treemap(df):
    """
    Generates an interactive treemap of AI Maturity Index by region.
    """
    fig = px.treemap(df, 
                     path=[px.Constant("world"), 'region', 'country_name'],
                     values='ai_maturity_index',
                     color='ai_maturity_index',
                     color_continuous_scale=px.colors.sequential.Plasma,
                     title="AI Maturity Index by Region")
    
    fig.write_html("visuals/ai_maturity_treemap.html")
    print("Interactive treemap saved to visuals/ai_maturity_treemap.html")

def create_interactive_scatter_plot(df):
    """
    Generates an interactive scatter plot of GDP vs Internet Usage, colored by AI Maturity Index.
    """
    fig = px.scatter(df,
                     x="gdp_per_capita",
                     y="internet_users_pct",
                     color="ai_maturity_index",
                     hover_name="country_name",
                     log_x=True,
                     size_max=60,
                     color_continuous_scale=px.colors.sequential.Plasma,
                     title="GDP vs. Internet Usage, Colored by AI Maturity Index")
    
    fig.write_html("visuals/ai_maturity_interactive_scatter_plot.html")
    print("Interactive scatter plot saved to visuals/ai_maturity_interactive_scatter_plot.html")

if __name__ == "__main__":
    # Load the processed data
    try:
        # NOTE: This script assumes 'country_name' and 'region' columns are available.
        # You may need to modify the data processing step to include this information.
        df_maturity = pd.read_csv('data/processed_data/ai_maturity_index.csv')
        df_gdp = pd.read_csv('data/raw_data/world_bank_gdp_per_capita.csv')
        df_internet = pd.read_csv('data/raw_data/world_bank_internet_users.csv')
    except FileNotFoundError:
        print("Error: Required CSV files not found. Please ensure 'process_data.py' has been run.")
        exit()

    # Data cleaning and type conversion
    df_maturity = df_maturity.dropna(subset=['country_iso'])
    df_maturity['country_iso'] = df_maturity['country_iso'].astype(str)

    # Clean and prepare GDP and internet data for merging
    df_gdp_latest = df_gdp.loc[df_gdp.groupby('country_iso')['year'].idxmax()]
    df_internet_latest = df_internet.loc[df_internet.groupby('country_iso')['year'].idxmax()]
    
    # --- Fix: Drop the 'internet_users_pct' and 'gdp_per_capita' columns from df_maturity to avoid merge conflicts ---
    df_maturity = df_maturity.drop(columns=['internet_users_pct', 'gdp_per_capita'])

    # Fix: Rename the 'value' column to 'gdp_per_capita' and 'internet_users_pct'
    df_gdp_latest = df_gdp_latest.rename(columns={'value': 'gdp_per_capita'})
    df_internet_latest = df_internet_latest.rename(columns={'value': 'internet_users_pct'})

    # Merge datasets to get full country names
    merged_df = pd.merge(df_maturity, df_gdp_latest[['country_iso', 'country_name', 'gdp_per_capita']], on='country_iso', how='left')
    merged_df = pd.merge(merged_df, df_internet_latest[['country_iso', 'internet_users_pct']], on='country_iso', how='left')

    # For the treemap, you would need a separate dataset mapping countries to regions.
    # For this demonstration, we'll create a placeholder.
    merged_df['region'] = merged_df['country_name'].apply(lambda x: 'Region A' if 'United States' in str(x) else 'Region B')

    # Create the advanced visualizations
    print("Generating advanced visualizations...")
    create_choropleth_map(merged_df)
    create_treemap(merged_df)
    create_interactive_scatter_plot(merged_df)
    
    print("All advanced visualizations have been generated and saved to the 'visuals/' directory as HTML files.")