import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def analyze_sleep_data():
    # Get the most recent CSV file from the downloads directory
    downloads_dir = Path(__file__).parent / "downloads"
    csv_files = list(downloads_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found in downloads directory")
    
    latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
    
    # Read the CSV file
    df = pd.read_csv(latest_file, header=0)

    # Convert date string to datetime
    df['date'] = pd.to_datetime(df['day'])
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['score'], marker='o', linestyle='-', linewidth=1, markersize=4)
    
    # Customize the plot
    plt.title('Sleep Score Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sleep Score')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    output_path = Path(__file__).parent / "sleep_analysis.png"
    plt.savefig(output_path)
    print(f"Analysis saved to: {output_path}")

if __name__ == "__main__":
    analyze_sleep_data() 