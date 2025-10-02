import orjson as json
import pandas as pd
from pathlib import Path
from tabulate import tabulate
from src.utils.env import load

def run_report():
    cfg = load()
    scored_dir = Path(cfg['project']['scored_dir'])
    in_file = scored_dir / "all_scored.jsonl"

    if not in_file.exists():
        print("No scored file found. Run scoring first.")
        return

    rows = []
    with open(in_file, "rb") as inp:
        for line in inp:
            record = json.loads(line)
            rows.append([
                record.get("indicator"),
                record.get("type"),
                record.get("score", 0),
                record.get("geo", {}).get("country", ""),
                record.get("geo", {}).get("asn", ""),
                record.get("source", "")
            ])

    if not rows:
        print("No records to report.")
        return

    df = pd.DataFrame(rows, columns=["Indicator", "Type", "Score", "Country", "ASN", "Source"])

    print("\n=== SAMPLE RECORDS PER SOURCE ===")
    for src, group in df.groupby("Source"):
        print(f"\nSource: {src}")
        print(tabulate(group.head(3), headers="keys", tablefmt="pretty"))

    print("\n=== SCORE DISTRIBUTION ===")
    print(df["Score"].describe())

    print("\n=== TOP COUNTRIES ===")
    print(df["Country"].value_counts().head(5))

    print("\n=== TOP SOURCES ===")
    print(df["Source"].value_counts())

    print("\n=== HIGH CONFIDENCE INDICATORS (Score > 70) ===")
    print(tabulate(df[df["Score"] > 70].head(10), headers="keys", tablefmt="pretty"))

if __name__ == "__main__":
    run_report()
