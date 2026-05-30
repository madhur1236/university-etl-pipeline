import requests
import pandas as pd
from sqlalchemy import create_engine
import os

url = "http://universities.hipolabs.com/search?country=United+States"

def extract_data(url) -> dict:
    data = requests.get(url).json()
    return data

def transform_data(data: dict) -> pd.DataFrame:
    "Used to transform the dataset into desired format"
    df = pd.DataFrame(data)
    print(f"Total number of universities in the US: {len(df)}")
    df = df[df["name"].str.contains("California", case=False, na=False)]
    print(f"Number of universities in California: {len(df)}")
    """df['domains'] = [','.join(map(str,l)) for l in df['domains']]
    df['web_pages'] = [','.join(map(str,l)) for l in df['web_pages']]
    df = df.reset_index(drop=True)
    return df[["domains","country","web_pages","name"]]""" 
    
    # Handle null values
    df['domains'] = df['domains'].apply(lambda x: x if isinstance(x, list) else [])
    df['web_pages'] = df['web_pages'].apply(lambda x: x if isinstance(x, list) else [])
    df['name'] = df['name'].fillna("Unknown")
    df['country'] = df['country'].fillna("Unknown")

    # Clean URLs
    def clean_urls(url_list):
        return [
            url.strip().lower().rstrip("/")
            for url in url_list if isinstance(url, str)
        ]

    df['domains'] = df['domains'].apply(clean_urls)
    df['web_pages'] = df['web_pages'].apply(clean_urls)

    # Convert list to string
    df['domains'] = df['domains'].apply(lambda x: ",".join(x))
    df['web_pages'] = df['web_pages'].apply(lambda x: ",".join(x))

    # Removing duplicates
    df = df.drop_duplicates(subset=["name", "domains"])

    # Reset index
    df = df.reset_index(drop=True)

    return df[[ "name", "country", "domains", "web_pages"]]


    
def load_data(df:pd.DataFrame) -> None:
        "Loads the data into sqllite database"
        os.makedirs("data", exist_ok=True)
        disk_engine = create_engine('sqlite:///data/universities.db')
        df.to_sql('universities', con=disk_engine, if_exists='replace', index=False)

def run_etl():
    data = extract_data(url)
    transformed = transform_data(data)
    load_data(transformed)
    return {
        "status": "success",
        "records": len(transformed)
    }