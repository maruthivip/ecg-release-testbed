import ast
import csv
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIELDS = (
    "id",
    "slide_item",
    "repository_or_fixture",
    "expected_nodes",
    "expected_edges",
    "observed_result",
    "status",
    "release_build",
)


class PreparationTests(unittest.TestCase):
    def test_matrix_has_complete_unique_rows_and_existing_fixtures(self):
        with (ROOT / "traceability.csv").open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            self.assertEqual(tuple(reader.fieldnames or ()), FIELDS)
            rows = list(reader)
        self.assertTrue(rows)
        ids = set()
        for row in rows:
            with self.subTest(case=row["id"]):
                self.assertNotIn(None, row)
                self.assertTrue(all(row.values()))
                self.assertNotIn(row["id"], ids)
                ids.add(row["id"])
                self.assertIn(row["status"], {"NOT_RUN", "BLOCKED", "PASS", "FAIL"})
                if row["repository_or_fixture"] != "NOT_PREPARED":
                    for fixture in row["repository_or_fixture"].split("; "):
                        self.assertTrue((ROOT / fixture).is_dir(), fixture)
                else:
                    self.assertNotEqual(row["status"], "PASS")
                if row["status"] in {"PASS", "FAIL"}:
                    self.assertNotEqual(row["release_build"], "UNKNOWN")
                    self.assertFalse(row["observed_result"].startswith("Not run"))

    def test_python_fixtures_parse(self):
        fixtures = list((ROOT / "fixtures").rglob("*.py"))
        self.assertTrue(fixtures)
        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                ast.parse(fixture.read_text(encoding="utf-8"), filename=str(fixture))

    def test_xml_and_json_fixtures_parse(self):
        for pattern in ("*.xml", "*.xhtml", "*.csproj"):
            for fixture in (ROOT / "fixtures").rglob(pattern):
                with self.subTest(fixture=fixture):
                    ET.parse(fixture)
        for fixture in (ROOT / "fixtures").rglob("package.json"):
            with self.subTest(fixture=fixture):
                json.loads(fixture.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
