import polars as pl
import plotly.graph_objects as go
from pathlib import Path


def analyze_sleep_data():
    # Get the most recent CSV file from the downloads directory
    downloads_dir = Path(__file__).parent / "downloads"
    csv_files = list(downloads_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found in downloads directory")

    csv_sleep_files = [file for file in csv_files if "daily-sleep" in file.name]

    latest_file = max(csv_sleep_files, key=lambda x: x.stat().st_mtime)

    # Read the CSV file using Polars instead of Pandas
    df = pl.read_csv(latest_file)

    # Convert date string to datetime using Polars syntax
    df = df.with_columns(pl.col("day").str.to_datetime().alias("date"))

    # Convert Polars DataFrame to lists for plotting
    dates = df.get_column("date").to_list()
    scores = df.get_column("score").to_list()

    # Create the plot using Plotly instead of Matplotlib
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=scores,
            mode="markers",
            name="Sleep Score",
            marker=dict(
                size=10,
                color=scores,
                opacity=0.8,
                colorscale=[
                    [0.0, "#cc0000"],  # Deep red for lowest values
                    [0.3, "#ff4400"],  # Red-orange
                    [0.7, "#ff8800"],  # Orange
                    [0.85, "#88cc00"],  # Yellow-green
                    [1.0, "#00cc00"],  # Deep green for highest values
                ],
                showscale=True,
                colorbar=dict(title="Sleep Score"),
            ),
        )
    )

    # Customize the plot
    fig.update_layout(
        title="Sleep Score Over Time",
        xaxis_title="Date",
        yaxis_title="Sleep Score",
        template="plotly_white",
    )

    # Save the plot as HTML for interactivity
    output_path = Path(__file__).parent / "sleep-analysis.html"
    fig.write_html(output_path)
    print(f"Analysis saved to: {output_path}")


if __name__ == "__main__":
    analyze_sleep_data()
