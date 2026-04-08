# API Data Pipeline (Python + SQL + Postman)

## Overview
End-to-end data pipeline that pulls workforce-related data from a public REST API, transforms it using Python, and loads it into a SQL Server database for reporting and analysis. Demonstrates the same API integration and data pipeline skills used in enterprise HRIS and IAM implementations.

## Problem
Organizations often need to pull data from external APIs (HRIS platforms, identity systems, third-party vendors) and load it into internal databases for reporting. Manual data transfers via SFTP are slow, error-prone, and hard to audit.

## Solution
- Built a Python script that calls a public REST API, handles authentication, and parses JSON responses
- Transforms and cleans the data using Python (pandas)
- Loads cleaned data into a SQL Server database
- Includes a Postman collection for manual API testing and validation
- SQL queries for analysis and reporting on the loaded data

## How This Relates to My Work
At DCU, I modernized 3 legacy SFTP integrations by converting them to REST APIs. I designed data mappings, API specs, and validated payloads using Postman. This project demonstrates that same workflow using a public API.

## Tools
- Python 3 (requests, pandas, json)
- SQL Server (SSMS)
- Postman (API testing and validation)
- REST API (JSONPlaceholder - free public API for testing)

## Files in This Repo
- `api_pipeline.py` - Python script that pulls, transforms, and loads API data
- `create_target_tables.sql` - SQL schema for the target database
- `analysis_queries.sql` - Queries to analyze the loaded data
- `postman_collection.json` - Postman collection for API endpoint testing
- `architecture.md` - Pipeline architecture documentation

## How to Run
1. Install Python 3 and pip
2. Run: pip install requests pandas
3. Run: python api_pipeline.py
4. Data will be saved to users_cleaned.csv (or load directly to SQL Server if configured)

## Author
Vijay Teli | [LinkedIn](https://www.linkedin.com/in/vijay-teli-581854145/)
