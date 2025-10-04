
# 🕵️‍♂️ Threat Intelligence Aggregation Lab

This project aggregates threat intelligence data from multiple open-source APIs like **AlienVault OTX, VirusTotal, Shodan, GreyNoise, and IPInfo**, then normalizes, enriches, scores, visualizes, and generates reports for analysis.

---

## 🚀 Setup Guide (For Team Members)

Follow these steps to set up and run the project on your local PC.

---

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/nigel-dsilva/osint-lab.git
cd osint-lab
````

### 2️⃣ Create a Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # On Windows
# OR
source .venv/bin/activate  # On Linux/Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install these manually:

```bash
pip install httpx orjson backoff python-dotenv networkx matplotlib reportlab
```

---

## 🔑 API Keys Setup

1. Copy the `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Edit `.env` and add your **API keys**:

```
OTX_API_KEY=your_alienvault_key
VT_API_KEY=your_virustotal_key
SHODAN_API_KEY=your_shodan_key
GREYNOISE_API_KEY=your_greynoise_key
IPINFO_TOKEN=your_ipinfo_key
```

👉 **Important:**

* Everyone can use the same keys, but **API limits will be hit faster**.
* If one key expires, another teammate can replace it in `.env`.
* Best practice: each member should add their **own keys** locally.

---

## 🛠 Running Collectors (Fetching Data)

Run collectors for different sources:

```bash
# AlienVault
python -m src.collectors.run_one alienvault_otx

# VirusTotal
python -m src.collectors.run_one virustotal

# Shodan
python -m src.collectors.run_one shodan

# GreyNoise
python -m src.collectors.run_one greynoise
```

📂 Data will be stored in:

```
data/raw/<source>/
```

---

## 🔄 Normalization, Enrichment & Merging
1. **Normalize the data:**

```bash
python -m src.normalizers.run_normalise
```   

2. **Enrich the normalized data:**

```bash
python -m src.enrichment.enrich_all
```

3. **Merge all sources:**

```bash
python -m src.merger.run_merge
```

4. **Score merged results:**

```bash
python -m src.scorers.run_score
```

📂 Outputs:

* Normalized data → `data/normalized/`
* Enriched data → `data/enriched/`
* Merged data → `data/merged/all.jsonl`
* Scored data → `data/scored/all_scored.jsonl`

---

## 📊 Graph Visualization

Generate correlation graphs between indicators:

```bash
python -m src.graphs.run_graph
```

📂 Graph files will be stored in:

```
data/correlation/
```

Open `.graphml` files with:

* [Gephi](https://gephi.org/)
* [Cytoscape](https://cytoscape.org/)
* Or load them in Python (NetworkX + Matplotlib).

---

## 📑 Report Generation

Generate PDF reports with summaries, statistics, and high-level findings:

```bash
python -m src.reports.run_report
```

📂 Reports will be saved in:

```
data/reports/
```

Reports include:

* Total indicators collected
* Distribution by source
* Enrichment details (GeoIP, ASN, etc.)
* Scoring summary (high/medium/low confidence indicators)
* Graph snapshots (if available)

👉 You can share these reports directly with your group or supervisors.

---

## 👥 Team Key Rotation (Important)

Since free APIs have **strict rate limits**:

* **AlienVault OTX:** ~500/day
* **VirusTotal:** 500/day
* **Shodan:** 1 request/min (Free tier)
* **GreyNoise:** 50/day
* **IPInfo:** 50k/month (Free tier)

⚡️ To avoid hitting limits:

* Each team member should use their **own API keys**.
* If one member’s quota is exhausted, another can update `.env` with their keys.
* Share keys **privately**, not on GitHub.

---

## ✅ Example Full Workflow (AlienVault → Report)

```bash
# Step 1: Collect from AlienVault
python -m src.collectors.run_one alienvault_otx

# Step 2: Enrich data
python -m src.enrichment.enrich_all

# Step 3: Merge all sources
python -m src.merger.run_merge

# Step 4: Score data
python -m src.scorers.run_score

# Step 5: Generate graph
python -m src.correlation.build_graph

# Step 6: Generate report
python -m src.reporting.basic_report
```

Output locations:

* Raw data → `data/raw/alienvault_otx/`
* Normalized data → `data/normalized/alienvault_otx/`
* Enriched data → `data/enriched/ipinfo_geo/`
* Merged → `data/merged/all.jsonl`
* Scored → `data/scored/all_scored.jsonl`
* Graphs → `data/correlation/*.graphml`
* Reports → `data/reports/*.pdf`

---

## 📌 Notes

* Keep `.env` **out of GitHub** (already in `.gitignore`).
* Rotate API keys in your team if limits are reached.
* Graph files can be opened in Gephi for visual analysis.
* Reports help summarize everything for presentation.

---

## 👨‍💻 Authors

* Group Project by **Nigel & Team**

