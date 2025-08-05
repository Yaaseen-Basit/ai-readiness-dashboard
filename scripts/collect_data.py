import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text # <-- This import is crucial
import pandas as pd
import os
import time

# Ensure the raw_data directory exists
if not os.path.exists('data/raw_data'):
    os.makedirs('data/raw_data')

def extract_pdf_text(pdf_path, output_path):
    """
    Extracts all text from a local PDF file and saves it to a text file.
    This function is necessary for your pipeline to work.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    try:
        print(f"Extracting text from PDF: {pdf_path}...")
        text = extract_text(pdf_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Successfully extracted text and saved to {output_path}")
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")

def get_world_bank_data(indicator_code, output_path, countries_list=None, retries=3, backoff_factor=2):
    """
    Fetches data from the World Bank API for a given indicator with a retry mechanism.
    If countries_list is None, it fetches data for all countries.
    """
    for attempt in range(retries):
        try:
            print(f"Fetching World Bank data for indicator '{indicator_code}'...")
            
            page = 1
            total_pages = 1
            all_records = []
            
            while page <= total_pages:
                url = f"http://api.worldbank.org/v2/country/all/indicator/{indicator_code}?format=json&per_page=500&page={page}"
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if data and isinstance(data, list) and len(data) > 1 and data[1]:
                    all_records.extend(data[1])
                    total_pages = data[0]['pages']
                    page += 1
                    time.sleep(1)
                else:
                    break

            if all_records:
                df = pd.DataFrame([
                    {'country_name': rec['country']['value'], 'country_iso': rec['countryiso3code'], 'year': rec['date'], 'value': rec['value']}
                    for rec in all_records if rec['value'] is not None
                ])

                if countries_list:
                    df = df[df['country_iso'].isin(countries_list)]
                    
                df.to_csv(output_path, index=False)
                print(f"Successfully fetched {len(df)} records for {len(df['country_iso'].unique())} countries and saved to {output_path}")
                return
            else:
                print(f"No records found for indicator '{indicator_code}' after all pages were checked.")
                return

        except requests.exceptions.Timeout as e:
            wait_time = backoff_factor ** attempt
            print(f"Timeout error on World Bank API call. Retrying in {wait_time} seconds... Error: {e}")
            time.sleep(wait_time)
        except requests.exceptions.RequestException as e:
            print(f"Non-timeout error fetching World Bank data: {e}")
            return
    
    print(f"Failed to fetch World Bank data after {retries} attempts.")

if __name__ == "__main__":
    # This list is now commented out as we are collecting data for all countries
    # target_countries_iso = ['USA','GBR','SGP','DEU','JPN','CHN','IND','BRA','AUS','CAN','FRA']
    
    # --- Data Collection Pipeline ---
    
    print("\n--- Starting Data Collection Pipeline ---")
    
    # This section remains unchanged
    print("\n[MANUAL ACTION REQUIRED]")
    print("McKinsey and IMF websites are blocking automated scraping.")
    print("Please manually download the 'Global Banking Annual Review' from McKinsey and the 'Global Financial Stability Report' from IMF.")
    print("Save these PDF files as `mckinsey_banking_report.pdf` and `imf_gfsr.pdf` into the `data/raw_data/` directory.")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get("https://www.oecd.ai/dashboards/policy-data", headers=headers, timeout=30)
        response.raise_for_status()
        with open('data/raw_data/oecd_ai_policy_data.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Successfully scraped OECD data.")
    except requests.exceptions.RequestException as e:
        print(f"Could not scrape OECD: {e}")
    
    print("\n--- Fetching Data from World Bank API for ALL COUNTRIES ---")
    
    # The `countries_list` parameter has been removed to fetch data for all countries
    get_world_bank_data(
        indicator_code='IT.NET.USER.ZS',
        output_path='data/raw_data/world_bank_internet_users.csv'
    )
    
    get_world_bank_data(
        indicator_code='NY.GDP.PCAP.KD',
        output_path='data/raw_data/world_bank_gdp_per_capita.csv'
    )
    
    print("\n--- Starting PDF Text Extraction ---")
    if os.path.exists('data/raw_data/imf_gfsr.pdf'):
        extract_pdf_text('data/raw_data/imf_gfsr.pdf', 'data/raw_data/imf_gfsr_text.txt')
    else:
        print("IMF PDF not found.")
    
    if os.path.exists('data/raw_data/mckinsey_banking_report.pdf'):
        extract_pdf_text('data/raw_data/mckinsey_banking_report.pdf', 'data/raw_data/mckinsey_banking_report_text.txt')
    else:
        print("McKinsey PDF not found.")