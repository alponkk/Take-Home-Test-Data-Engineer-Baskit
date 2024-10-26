# Data Engineer Project: ETL Pipeline from Google Sheets to SQLite

This project demonstrates an ETL pipeline that extracts data from Google Sheets, performs necessary transformations, and loads the data into an SQLite database. The project consists of two implementations:
1. A standalone Python script version.
2. An Airflow DAG version for automated scheduling and task management.

## Table of Contents
- [Data Understanding](#data-understanding)
- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)

---

## Data Understanding

The dataset used in this project is a sample table from a Google Sheet, which contains the following columns:
- `id`: A unique identifier for each record.
- `name`: Name of the individual.
- `phone_number`: The individual's contact number, which requires cleaning as the values are inconsistent in format.
- `born_day`: The date of birth of each individual, with mixed formats (e.g., `YYYY-MM-DD` or `YYYY/MM/DD`), requiring date format standardization.

### Sample Data (born_date_data)

| id       | name   | phone_number | born_day   |
|----------|--------|--------------|------------|
| ab10212  | Blair  | 81883494035  | 1987-11-20 |
| ab10213  | Kurt   | 6281615589027| 1991-04-06 |
| ab10214  | Brain  | 6281429780440| 1992-04-13 |
| ...      | ...    | ...          | ...        |

### Transformation Objectives
1. **Phone Number Cleaning**: Standardize phone numbers to an international format by removing non-numeric characters and ensuring all numbers start with `62` (Indonesia’s country code).
2. **Date Format Standardization**: Convert all birthdates into the `YYYY-MM-DD` format for consistency and compatibility with SQLite.

---

## Project Overview

### Objective
The ETL pipeline aims to automate the extraction of data from Google Sheets, clean and transform the data, and load it into an SQLite database for further analysis or storage.

### ETL Steps
1. **Extract**: Retrieve data from a specified Google Sheets document using `gspread` and load it into a Pandas DataFrame.
2. **Transform**: 
   - Clean and standardize the `phone_number` field.
   - Reformat the `born_day` field to ensure consistent date formatting.
3. **Load**: Insert the transformed data into an SQLite database table called `born_date_data`.

### ETL Pipeline Option
1. Create ETL using python script and schedule using windowsk task scheduler tu run ETL script daily.
2. Create DAG using Apache Airflow to schedule DAG daily.

---

## Prerequisites
- Python
- SQLite3
- Apache Airflow
- Google Service Account for Google Sheets access (download JSON key file).
- Google Sheets with shared access to our Google Service Account.

### Required Libraries
Install the required libraries:
```bash
pip install gspread pandas sqlite3 apache-airflow
```

## Project Structure
- **baskit/etl_born_date_cleaning.py**: Standalone Python script that performs the ETL process.
- **baskit/etl_born_date_cleaning_dag.py**: Airflow DAG script for scheduling and running the ETL tasks.
- **service_account_creds**(not included): Configuration details for accessing Google Sheets (Service Account JSON file).
- **db**: SQLite3 Database.

## Results
baskit/etl_born_date_cleaning.py 
```
Output:
--- EXTRACT START ---
--- EXTRACT SUCCESS ---
--- TRANSFORM START ---
--- TRANSFORM SUCCESS ---
--- LOAD SUCCESS ---
--- LOAD SUCCESS ---
        id    name   phone_number    born_day
0  ab10212   Blair  6281883494035  1987-11-20
1  ab10213    Kurt  6281615589027  1991-04-06
2  ab10214   Brain  6281429780440  1992-04-13
3  ab10215    Seth  6281716992765  1989-01-04
4  ab10216   Madge  6281902482399  1990-08-11
5  ab10217  Claire  6281525434419  2007-12-05
6  ab10218    Jill  6281584489426  2008-02-16
7  ab10219    Josh  6281674056264  1995-05-17
8  ab10220   Merle  6281749431137  1995-12-12
9  ab10221    Gale  6281660050569  1996-04-23
```


baskit/etl_born_date_cleaning_dag.py - Airflow UI:

![image](https://github.com/user-attachments/assets/6c2d8740-ce50-4f4b-94a1-8659bf51d18e)



born_date_data table - SQLite3 in DBeaver:

![image](https://github.com/user-attachments/assets/6ce15f14-27bc-485b-ae1f-d7f79e8fa74e)

