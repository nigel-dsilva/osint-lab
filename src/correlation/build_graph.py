# src/correlation/build_graph.py
import orjson as json
import networkx as nx
from pathlib import Path
from src.utils.env import load

def sanitize(value):
    return "" if value is None else value

def build_graph():
    cfg = load()
    scored_dir = Path(cfg['project']['scored_dir'])
    corr_dir = Path(cfg['project']['correlation_dir'])
    corr_dir.mkdir(parents=True, exist_ok=True)

    in_file = scored_dir / "all_scored.jsonl"
    out_graphml = corr_dir / "all.graphml"

    if not in_file.exists():
        raise SystemExit(f"No scored file found: {in_file}")

    G = nx.Graph()
    with open(in_file, "rb") as inp:
        for line in inp:
            record = json.loads(line)
            ind = sanitize(record.get("indicator"))
            ind_type = sanitize(record.get("type"))
            score = record.get("score", 0) or 0
            source = sanitize(record.get("source", ""))

            if ind:
                G.add_node(ind, type=ind_type, score=score, source=source)

                for ref in record.get("references", []):
                    ref = sanitize(ref)
                    if ref:
                        G.add_node(ref, type="reference")
                        G.add_edge(ind, ref, relation="mentioned_with")

                if "geo" in record and record["geo"].get("asn"):
                    asn = sanitize(record["geo"]["asn"])
                    if asn:
                        G.add_node(asn, type="asn")
                        G.add_edge(ind, asn, relation="belongs_to")

    nx.write_graphml(G, out_graphml)
    print(f"Graph built -> {out_graphml}, Nodes={len(G.nodes)}, Edges={len(G.edges)}")

if __name__ == "__main__":
    build_graph()
