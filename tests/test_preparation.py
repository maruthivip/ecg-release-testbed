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
        fixtures = [
            path
            for directory in ("fixtures", "scenarios")
            for path in (ROOT / directory).rglob("*.py")
        ]
        self.assertTrue(fixtures)
        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                ast.parse(fixture.read_text(encoding="utf-8"), filename=str(fixture))

    def test_xml_and_json_fixtures_parse(self):
        for directory in ("fixtures", "scenarios"):
            for pattern in ("*.xml", "*.xhtml", "*.csproj"):
                for fixture in (ROOT / directory).rglob(pattern):
                    with self.subTest(fixture=fixture):
                        ET.parse(fixture)
            for fixture in (ROOT / directory).rglob("package.json"):
                with self.subTest(fixture=fixture):
                    json.loads(fixture.read_text(encoding="utf-8"))

    def test_order_lifecycle_assertion_anchors(self):
        scenario = ROOT / "scenarios" / "order_lifecycle"
        document = json.loads((scenario / "assertions.json").read_text(encoding="utf-8"))
        with (ROOT / "traceability.csv").open(encoding="utf-8", newline="") as stream:
            matrix_ids = {row["id"] for row in csv.DictReader(stream)}
        self.assertEqual(document["schema_version"], 1)
        self.assertEqual(document["status"], "NOT_RUN")
        ids = set()
        expectations = set()
        for case in document["assertions"]:
            with self.subTest(case=case["id"]):
                self.assertNotIn(case["id"], ids)
                ids.add(case["id"])
                self.assertIn(case["matrix_id"], matrix_ids)
                self.assertIn(case["expectation"], {"present", "absent"})
                expectations.add(case["expectation"])
                self.assertTrue(case["relationship"])
                self.assertTrue(case["note"])
                for endpoint in ("source", "target"):
                    reference = (scenario / case[endpoint]["file"]).resolve()
                    self.assertTrue(reference.is_relative_to(scenario.resolve()))
                    self.assertTrue(reference.is_file())
                    self.assertIn(case[endpoint]["anchor"], reference.read_text(encoding="utf-8"))
        self.assertEqual(expectations, {"present", "absent"})

    def test_impact_questions_have_evidence(self):
        scenario = ROOT / "scenarios" / "impact_lab"
        document = json.loads((scenario / "questions.json").read_text(encoding="utf-8"))
        self.assertEqual(document["schema_version"], 1)
        ids = set()
        for case in document["cases"]:
            with self.subTest(case=case["id"]):
                self.assertNotIn(case["id"], ids)
                ids.add(case["id"])
                for field in ("question", "expected", "required", "forbidden_claims", "evidence"):
                    self.assertTrue(case[field], field)
                for item in case["evidence"]:
                    reference = (scenario / item["file"]).resolve()
                    self.assertTrue(reference.is_relative_to(scenario.resolve()))
                    self.assertTrue(reference.is_file())
                    self.assertIn(item["anchor"], reference.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(ids), 10)


if __name__ == "__main__":
    unittest.main()
