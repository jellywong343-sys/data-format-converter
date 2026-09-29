import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from data_format_converter.cli import read_records, write_records

class ConverterTests(unittest.TestCase):
    def test_csv_json_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_path, json_path, csv_again = root / "data.csv", root / "data.json", root / "again.csv"
            csv_path.write_text("name,age\nAlice,30\nBob,40\n", encoding="utf-8")
            records = read_records(csv_path, "csv", encoding="utf-8", delimiter=",")
            write_records(json_path, "json", records)
            loaded = read_records(json_path, "json", encoding="utf-8")
            write_records(csv_again, "csv", loaded)
            self.assertEqual(loaded[0]["name"], "Alice")
            self.assertIn("Bob,40", csv_again.read_text(encoding="utf-8"))

    def test_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.jsonl"
            write_records(path, "jsonl", [{"id": 1}, {"id": 2}])
            self.assertEqual(read_records(path, "jsonl", encoding="utf-8"), [{"id": 1}, {"id": 2}])

if __name__ == "__main__": unittest.main()
