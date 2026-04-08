"""
API Data Pipeline
Author: Vijay Teli
Purpose: Pull data from REST API, transform, and load into structured format

This demonstrates the same workflow used in enterprise HRIS integrations:
1. Call API endpoint and handle authentication/errors
2. Parse JSON response
3. Transform and clean data
4. Load into target database or file
"""

import requests
import pandas as pd
import json
from datetime import datetime


def extract_from_api(url):
    """Pull data from REST API endpoint with error handling"""
    print(f"[{datetime.now()}] Calling API: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"[{datetime.now()}] SUCCESS - Retrieved {len(data)} records")
        return data
        
    except requests.exceptions.HTTPError as e:
        print(f"[{datetime.now()}] HTTP Error: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"[{datetime.now()}] Connection Error: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"[{datetime.now()}] Timeout Error: {e}")
        return None


def transform_users(raw_data):
    """Transform and clean user data"""
    print(f"[{datetime.now()}] Transforming {len(raw_data)} user records...")
    
    df = pd.DataFrame(raw_data)
    
    # Flatten nested address object
    df['street'] = df['address'].apply(lambda x: x.get('street', ''))
    df['city'] = df['address'].apply(lambda x: x.get('city', ''))
    df['zipcode'] = df['address'].apply(lambda x: x.get('zipcode', ''))
    df['lat'] = df['address'].apply(lambda x: x.get('geo', {}).get('lat', ''))
    df['lng'] = df['address'].apply(lambda x: x.get('geo', {}).get('lng', ''))
    
    # Flatten nested company object
    df['company_name'] = df['company'].apply(lambda x: x.get('name', ''))
    df['company_bs'] = df['company'].apply(lambda x: x.get('bs', ''))
    
    # Drop original nested columns
    df = df.drop(columns=['address', 'company'])
    
    # Clean and standardize
    df['name'] = df['name'].str.strip().str.title()
    df['email'] = df['email'].str.strip().str.lower()
    df['city'] = df['city'].str.strip().str.title()
    
    # Add metadata
    df['extracted_date'] = datetime.now().strftime('%Y-%m-%d')
    df['source'] = 'JSONPlaceholder API'
    
    # Validate no nulls in required fields
    required = ['id', 'name', 'email']
    null_check = df[required].isnull().sum()
    if null_check.sum() > 0:
        print(f"[{datetime.now()}] WARNING - Null values found: {null_check.to_dict()}")
    else:
        print(f"[{datetime.now()}] VALIDATION PASSED - No nulls in required fields")
    
    print(f"[{datetime.now()}] Transform complete - {len(df)} records, {len(df.columns)} columns")
    return df


def transform_posts(raw_data):
    """Transform post data and add analytics"""
    print(f"[{datetime.now()}] Transforming {len(raw_data)} post records...")
    
    df = pd.DataFrame(raw_data)
    
    # Clean text fields
    df['title'] = df['title'].str.strip().str.capitalize()
    df['body'] = df['body'].str.strip()
    
    # Add analytics columns
    df['title_word_count'] = df['title'].str.split().str.len()
    df['body_word_count'] = df['body'].str.split().str.len()
    df['extracted_date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Aggregate posts per user
    user_post_counts = df.groupby('userId').size().reset_index(name='total_posts')
    df = df.merge(user_post_counts, on='userId', how='left')
    
    print(f"[{datetime.now()}] Transform complete - {len(df)} records")
    return df


def load_to_csv(df, filename):
    """Load transformed data to CSV (simulates database load)"""
    filepath = f"{filename}"
    df.to_csv(filepath, index=False)
    print(f"[{datetime.now()}] LOADED {len(df)} records to {filepath}")
    return filepath


def run_pipeline():
    """Main pipeline orchestrator"""
    print("=" * 60)
    print("API DATA PIPELINE - Starting")
    print("=" * 60)
    
    # Extract
    users_raw = extract_from_api("https://jsonplaceholder.typicode.com/users")
    posts_raw = extract_from_api("https://jsonplaceholder.typicode.com/posts")
    
    if users_raw is None or posts_raw is None:
        print("Pipeline FAILED - API extraction errors")
        return
    
    # Transform
    users_clean = transform_users(users_raw)
    posts_clean = transform_posts(posts_raw)
    
    # Load
    load_to_csv(users_clean, "users_cleaned.csv")
    load_to_csv(posts_clean, "posts_cleaned.csv")
    
    # Summary
    print("=" * 60)
    print("PIPELINE COMPLETE")
    print(f"  Users: {len(users_clean)} records extracted and loaded")
    print(f"  Posts: {len(posts_clean)} records extracted and loaded")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
