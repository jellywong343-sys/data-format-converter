from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

FORMATS = {"csv", "json", "jsonl"}


def infer_format(path: Path) -> str:
    suffix = path.suffix.lower()
    mapping = {".csv": "csv", ".json": "json", ".jsonl": "jsonl", ".ndjson": "jsonl"}
    if suffix not in mapping:
        raise ValueError(f"Cannot infer format from extension: {path}")
    return mapping[suffix]


def read_records(path: Path, fmt: str, encoding: str = "utf-8-sig", delimiter: str = ",") -> list[dict[str, Any]]:
    if fmt not in FORMATS:
        raise ValueError(f"Unsupported input format: {fmt}")
    if fmt == "csv":
        sample = path.read_text(encoding=encoding)[:8192]
        if delimiter == "auto":
            try:
                delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
            except csv.Error:
                delimiter = ","
        with path.open("r", encoding=encoding, newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            if not reader.fieldnames:
                raise ValueError("CSV has no header")
            return [{(key or "").strip(): value or "" for key, value in row.items()} for row in reader]
    if fmt == "json":
        data = json.loads(path.read_text(encoding=encoding))
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
            raise ValueError("JSON input must be an object or an array of objects")
        return data
    records = []
    for number, line in enumerate(path.read_text(encoding=encoding).splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        if not isinstance(item, dict):
            raise ValueError(f"JSONL line {number} is not an object")
        records.append(item)
    return records


def field_order(records: list[dict[str, Any]]) -> list[str]:
    fields: list[str] = []
    for row in records:
        for key in row:
            if key not in fields:
                fields.append(key)
    return fields


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def write_records(path: Path, fmt: str, records: list[dict[str, Any]],
                  encoding: str = "utf-8", delimiter: str = ",", pretty: bool = True) -> None:
    if fmt not in FORMATS:
        raise ValueError(f"Unsupported output format: {fmt}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "csv":
        fields = field_order(records)
        if not fields:
            raise ValueError("Cannot write CSV without any fields")
        with path.open("w", encoding=encoding, newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter=delimiter)
            writer.writeheader()
            for row in records:
                writer.writerow({field: csv_value(row.get(field)) for field in fields})
    elif fmt == "json":
        text = json.dumps(records, ensure_ascii=False, indent=2 if pretty else None, separators=None if pretty else (",", ":"))
        path.write_text(text + ("\n" if pretty else ""), encoding=encoding)
    else:
        with path.open("w", encoding=encoding, newline="\n") as handle:
            for row in records:
                handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert records between CSV, JSON, and JSON Lines.")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--from", dest="input_format", choices=sorted(FORMATS))
    parser.add_argument("--to", dest="output_format", choices=sorted(FORMATS))
    parser.add_argument("--input-encoding", default="utf-8-sig")
    parser.add_argument("--output-encoding", default="utf-8")
    parser.add_argument("--input-delimiter", default="auto")
    parser.add_argument("--output-delimiter", default=",")
    parser.add_argument("--compact", action="store_true", help="Write compact JSON")
    args = parser.parse_args()
    source, target = Path(args.input), Path(args.output)
    input_format = args.input_format or infer_format(source)
    output_format = args.output_format or infer_format(target)
    records = read_records(source, input_format, args.input_encoding, args.input_delimiter)
    write_records(target, output_format, records, args.output_encoding, args.output_delimiter, not args.compact)
    print(f"Converted {len(records)} records: {input_format} -> {output_format}")
    print(f"Output: {target.resolve()}")

if __name__ == "__main__": main()
