# Data Format Converter

[绠€浣撲腑鏂嘳(README.zh-CN.md)

Convert record-oriented data between CSV, JSON arrays, and JSON Lines (JSONL/NDJSON).

## Features

- CSV to JSON or JSONL.
- JSON arrays or single objects to CSV/JSONL.
- JSONL to CSV or JSON.
- Input/output encoding controls.
- Automatic CSV delimiter detection or explicit delimiters.
- Preserves nested JSON values in CSV as compact JSON text.

## Install

```bash
git clone https://github.com/jellywong343-sys/data-format-converter.git
cd data-format-converter
python -m pip install -e .
```

## Usage

```bash
data-convert examples/products.csv products.json
data-convert products.json products.jsonl
data-convert products.jsonl products.csv
data-convert legacy.csv output.json --input-encoding gb18030
data-convert data.txt result.csv --from jsonl --to csv
```

The output file is replaced if it already exists. Keep a backup when converting important data.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT


