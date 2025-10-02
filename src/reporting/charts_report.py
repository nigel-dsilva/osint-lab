import pandas as pd
import matplotlib.pyplot as plt
from src.storage import db

def run_charts():
    rows = db.query("SELECT indicator, type, score, country, asn, source FROM indicators")
    if not rows:
        print("No records in DB. Run pipeline first.")
        return

    df = pd.DataFrame(rows, columns=["Indicator", "Type", "Score", "Country", "ASN", "Source"])

    # === Histogram of Scores ===
    plt.figure(figsize=(6,4))
    df["Score"].hist(bins=10, edgecolor="black")
    plt.title("Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

    # === Top Countries Bar Chart ===
    plt.figure(figsize=(6,4))
    df["Country"].value_counts().head(5).plot(kind="bar")
    plt.title("Top 5 Countries by Indicator Count")
    plt.xlabel("Country")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_charts()
