import polars as pl
import matplotlib.pyplot as plt
from pathlib import Path


def analyze_sleep_data():
    # Get the most recent CSV file from the downloads directory
    downloads_dir = Path(__file__).parent / "downloads"
    csv_files = list(downloads_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found in downloads directory")

    latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)

    # Read the CSV file using Polars instead of Pandas
    df = pl.read_csv(latest_file)

    # Convert date string to datetime using Polars syntax
    df = df.with_columns(pl.col("day").str.to_datetime().alias("date"))

    # Convert Polars DataFrame to lists for plotting
    dates = df.get_column("date").to_list()
    scores = df.get_column("score").to_list()

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(dates, scores, marker="o", linestyle="-", linewidth=1, markersize=4)

    # Customize the plot
    plt.title("Sleep Score Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sleep Score")
    plt.grid(True, linestyle="--", alpha=0.7)

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
