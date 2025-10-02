"""
Master Orchestrator for OSINT Pipeline
Runs the full sequence: Collect -> Normalize -> Enrich -> Merge -> Score -> Correlate -> Store -> Report
"""

import subprocess
import sys

STEPS = [
    # 1. Collectors
    ["python", "-m", "src.collectors.run_all"],

    # 2. Normalizers
    ["python", "-m", "src.normalizers.run_all"],

    # 3. Enrichment
    ["python", "-m", "src.enrichment.enrich_all"],

    # 4. Merge
    ["python", "-m", "src.merge.merge_all"],

    # 5. Score
    ["python", "-m", "src.scorers.run_score"],

    # 6. Correlation
    ["python", "-m", "src.correlation.build_graph"],

    # 7. Store in DB
    ["python", "-m", "src.storage.load_scored"],

    # 8. Generate Reports
    ["python", "-m", "src.reporting.export_report"],
    ["python", "-m", "src.reporting.charts_report"],
    ["python", "-m", "src.reporting.graph_preview"]
]

def run_pipeline():
    for step in STEPS:
        print("\n" + "="*60)
        print(">>> Running:", " ".join(step))
        print("="*60)
        try:
            subprocess.run(step, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Step failed: {' '.join(step)}")
            sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
