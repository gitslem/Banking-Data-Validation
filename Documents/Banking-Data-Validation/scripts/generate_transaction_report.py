import pandas as pd
import matplotlib.pyplot as plt
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='report_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_issues(file_path):
    """Load transaction issues from CSV."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loaded issues from {file_path}. Total rows: {len(df)}")
        return df
    except Exception as e:
        logging.error(f"Failed to load issues: {e}")
        return pd.DataFrame()

def generate_summary_report(df):
    """Generate a summary report of transaction issues."""
    if df.empty:
        logging.warning("No data to generate report.")
        return None

    # Summarize issues by type
    summary = df.groupby('issue_type').agg(
        issue_count=('transaction_id', 'count'),
        total_amount=('amount', 'sum')
    ).reset_index()

    return summary

def plot_issues(summary, output_dir):
    """Create a bar chart of issue counts by type."""
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(summary['issue_type'], summary['issue_count'], color='#1f77b4')
        plt.xlabel('Issue Type')
        plt.ylabel('Number of Issues')
        plt.title('Transaction Issues Summary')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        output_file = f"{output_dir}/issues_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(output_file)
        plt.close()
        logging.info(f"Chart saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to generate chart: {e}")

def main():
    # Input and output paths
    input_file = "transaction_issues_latest.csv"  # Replace with actual file path
    output_dir = "reports"

    # Load data
    df = load_issues(input_file)
    if df.empty:
        return

    # Generate summary report
    summary = generate_summary_report(df)
    if summary is not None:
        output_file = f"{output_dir}/summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        summary.to_csv(output_file, index=False)
        logging.info(f"Summary report saved to {output_file}")

        # Generate visualization
        plot_issues(summary, output_dir)

if __name__ == "__main__":
    try:
        main()
        logging.info("Reporting script completed successfully.")
    except Exception as e:
        logging.error(f"Script failed: {e}")
