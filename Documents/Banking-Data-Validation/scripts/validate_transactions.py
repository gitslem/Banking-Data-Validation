import psycopg2
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='validation_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database connection parameters
DB_PARAMS = {
    'dbname': 'banking_db',
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

def connect_db():
    """Connect to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        logging.info("Successfully connected to the database.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        raise

def run_validation_query(query, conn, query_name):
    """Execute a validation query and return results as a DataFrame."""
    try:
        df = pd.read_sql(query, conn)
        logging.info(f"{query_name} executed successfully. Found {len(df)} issues.")
        return df
    except Exception as e:
        logging.error(f"Error executing {query_name}: {e}")
        return pd.DataFrame()

def main():
    # Define validation queries
    queries = {
        "Negative Amount Transactions": """
            SELECT transaction_id, account_id, amount, transaction_date, type
            FROM transactions
            WHERE amount <= 0
            ORDER BY transaction_date DESC;
        """,
        "Orphaned Transactions": """
            SELECT t.transaction_id, t.account_id, t.transaction_date, t.type
            FROM transactions t
            LEFT JOIN accounts a ON t.account_id = a.account_id
            WHERE a.account_id IS NULL;
        """,
        "Stale Pending Transactions": """
            SELECT transaction_id, account_id, transaction_date, status
            FROM transactions
            WHERE status = 'PENDING'
            AND transaction_date < NOW() - INTERVAL '24 hours'
            ORDER BY transaction_date;
        """
    }

    # Connect to database
    conn = connect_db()
    cursor = conn.cursor()

    # Run validation queries and store results
    all_issues = []
    for query_name, query in queries.items():
        df = run_validation_query(query, conn, query_name)
        if not df.empty:
            df['issue_type'] = query_name
            all_issues.append(df)

    # Combine results and save to CSV
    if all_issues:
        combined_issues = pd.concat(all_issues, ignore_index=True)
        output_file = f"transaction_issues_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        combined_issues.to_csv(output_file, index=False)
        logging.info(f"Issues saved to {output_file}. Total issues: {len(combined_issues)}")
    else:
        logging.info("No issues found in validation.")

    # Close database connection
    cursor.close()
    conn.close()
    logging.info("Database connection closed.")

if __name__ == "__main__":
    try:
        main()
        logging.info("Validation script completed successfully.")
    except Exception as e:
        logging.error(f"Script failed: {e}")
