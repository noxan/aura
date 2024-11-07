import polars as pl
import plotly.graph_objects as go
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

    # Create the plot using Plotly instead of Matplotlib
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=scores,
            mode="markers",
            name="Sleep Score",
            marker=dict(
                size=6,
                color=scores,
                colorscale="RdYlGn",
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
    output_path = Path(__file__).parent / "sleep_analysis.html"
    fig.write_html(output_path)
    print(f"Analysis saved to: {output_path}")


if __name__ == "__main__":
    analyze_sleep_data()
