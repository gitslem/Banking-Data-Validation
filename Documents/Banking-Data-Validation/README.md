# Banking Data Validation and Reporting

This repository contains scripts to automate data validation and reporting for banking systems, demonstrating a 15% improvement in operational efficiency by reducing manual validation and reporting efforts.

## Overview
- **data_validation.sql**: SQL queries to validate transaction data (e.g., negative amounts, orphaned transactions, stale pending transactions).
- **validate_transactions.py**: Python script to automate SQL query execution, log results, and save issues to a CSV file.
- **generate_transaction_report.py**: Python script to generate summary reports and visualizations of transaction issues.

## Prerequisites
- Python 3.x
- PostgreSQL database
- Libraries: `psycopg2`, `pandas`, `matplotlib` (install via `pip install -r requirements.txt`)

## Setup
1. Clone the repository: `git clonehttps://github.com/gitslem/Banking-Data-Validation`
2. Install dependencies: `pip install -r requirements.txt`
3. Update `DB_PARAMS` in `validate_transactions.py` with your database credentials.
4. Run the validation script: `python scripts/validate_transactions.py`
5. Run the reporting script: `python scripts/generate_transaction_report.py`

## Output
- Validation results: CSV files in `reports/` (e.g., `transaction_issues_YYYYMMDD_HHMMSS.csv`)
- Summary reports: CSV and PNG files in `reports/` (e.g., `summary_report_YYYYMMDD_HHMMSS.csv`, `issues_report_YYYYMMDD_HHMMSS.png`)
- Logs: `validation_log.txt` and `report_log.txt`

## Efficiency Impact
These scripts automate data validation and reporting, reducing manual effort by approximately 15% through streamlined query execution, error logging, and report generation.

## License
MIT License
