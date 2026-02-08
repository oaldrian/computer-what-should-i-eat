#!/usr/bin/env python3
"""
Convert a CSV of base items into a JSON array suitable for embedding as builtinItems.

Usage:
  python scripts/csv_to_base.py data/base_items.csv --out data/builtin_items.json

CSV format (example header):
  id,name,rating,note,sweet,carb,meat

Any columns after the known columns will become attributes (key: value).
If `id` is empty, a UUID-based id will be generated.
"""
from __future__ import annotations
import csv
import json
import argparse
import uuid
import re
from pathlib import Path

KNOWN = ["id", "name", "rating", "note"]


def make_id(name: str) -> str:
    # fallback id generator: uuid4 hex prefix
    return "b-" + uuid.uuid4().hex[:8]


def parse_row(row: dict) -> dict:
    item = {}
    item_id = (row.get("id") or "").strip()
    name = (row.get("name") or "").strip()
    if not item_id:
        item_id = make_id(name or "item")
    item["id"] = item_id
    item["name"] = name
    rating_raw = (row.get("rating") or "").strip()
    if rating_raw:
        try:
            item["rating"] = int(rating_raw)
        except Exception:
            # keep as string if not integer
            item["rating"] = rating_raw
    note = (row.get("note") or "").strip()
    if note:
        item["note"] = note

    # attributes are any remaining columns not in KNOWN
    attrs = {}
    for k, v in row.items():
        if not k:
            continue
        lk = k.strip()
        if lk in KNOWN:
            continue
        val = (v or "").strip()
        if val != "":
            attrs[lk] = val
    if attrs:
        item["attributes"] = attrs
    return item


def csv_to_json(inpath: Path, outpath: Path):
    items = []
    # open with 'utf-8-sig' to remove possible BOM and require semicolon delimiter
    with inpath.open(newline='', encoding='utf-8-sig') as fh:
        # read a sample to detect delimiter; require ';' explicitly
        sample = fh.read(4096)
        fh.seek(0)
        try:
            sniff = csv.Sniffer().sniff(sample)
            detected = sniff.delimiter
        except Exception:
            detected = None
        if detected and detected != ';':
            print(f"ERROR: detected delimiter '{detected}' in CSV — this tool only accepts ';' separated files")
            raise SystemExit(2)
        reader = csv.DictReader(fh, delimiter=';')
        for r in reader:
            # skip completely empty rows
            if not any((v or '').strip() for v in r.values()):
                continue
            items.append(parse_row(r))
    # write JSON array
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open('w', encoding='utf-8') as fh:
        json.dump(items, fh, ensure_ascii=False, indent=2)
    print(f"Wrote {len(items)} items to {outpath}")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Convert CSV to builtin items JSON')
    p.add_argument('csv', help='input CSV file')
    p.add_argument('--out', '-o', help='output JSON file', default='data/builtin_items.json')
    args = p.parse_args()
    inpath = Path(args.csv)
    outpath = Path(args.out)
    if not inpath.exists():
        print(f"ERROR: input file {inpath} does not exist")
        raise SystemExit(1)
    csv_to_json(inpath, outpath)
