from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "projects"
TEMPLATE = ROOT / "mapa" / "map-fragment.template.html"
sys.path.insert(0, str(ROOT / "mapa" / "scripts"))

import build_map  # noqa: E402


class SanitizedProjectFixtureTest(unittest.TestCase):
    fixture_names = ("single-xy", "multi-yx")

    def test_fixture_metadata_is_complete_sanitized_and_spatially_distinct(self) -> None:
        metadata = [
            json.loads((FIXTURES / name / "fixture-metadata.json").read_text(encoding="utf-8"))
            for name in self.fixture_names
        ]

        for item in metadata:
            self.assertEqual(item["schemaVersion"], 1)
            self.assertFalse(item["containsPrivateData"])
            self.assertEqual(item["provenance"], "Fully synthetic; no external snapshot or private data.")
            self.assertEqual(len(item["spatial"]["bbox"]), 4)
            self.assertIn(item["spatial"]["gmlCoordinateOrder"], {"xy", "yx"})
            self.assertIn(item["spatial"]["wms130AxisOrder"], {"xy", "yx"})

        self.assertEqual({item["subject"] for item in metadata}, {"single-parcel", "multi-parcel"})
        self.assertEqual({item["location"] for item in metadata}, {"synthetic-west", "synthetic-east"})
        self.assertEqual({item["spatial"]["crs"] for item in metadata}, {"EPSG:2180", "EPSG:2178"})
        self.assertEqual({item["spatial"]["gmlCoordinateOrder"] for item in metadata}, {"xy", "yx"})

    def test_reference_builder_builds_each_fixture_without_source_code_changes(self) -> None:
        for fixture_name in self.fixture_names:
            with self.subTest(fixture=fixture_name), tempfile.TemporaryDirectory() as directory:
                map_dir = Path(directory) / fixture_name
                shutil.copytree(FIXTURES / fixture_name, map_dir)
                shutil.copy2(TEMPLATE, map_dir / TEMPLATE.name)
                manual_collection = {
                    "type": "FeatureCollection",
                    "features": [{
                        "type": "Feature",
                        "properties": {"id": "runtime-test-line", "name": "Synthetic path"},
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[1, 1], [2, 2], [3, 1]],
                        },
                    }],
                }
                (map_dir / "manual-overlays.json").write_text(
                    json.dumps(manual_collection),
                    encoding="utf-8",
                )

                fragment_path, standalone_path = build_map.build(map_dir)
                first_fragment = fragment_path.read_text(encoding="utf-8")
                first_standalone = standalone_path.read_text(encoding="utf-8")
                build_map.build(map_dir)

                self.assertNotRegex(first_fragment, r"__[A-Z][A-Z_]+__")
                self.assertEqual(fragment_path.read_text(encoding="utf-8"), first_fragment)
                self.assertEqual(standalone_path.read_text(encoding="utf-8"), first_standalone)
                self.assertTrue((map_dir / "manual-overlays.json").exists())

                project = build_map.validate_project_config(
                    build_map.load_json(map_dir / "project-config.json")
                )
                metadata = build_map.load_json(map_dir / "fixture-metadata.json")
                self.assertIn(
                    json.dumps(project, ensure_ascii=False, separators=(",", ":")),
                    first_fragment,
                )
                self.assertIn(
                    json.dumps(manual_collection, ensure_ascii=False, separators=(",", ":")),
                    first_fragment,
                )
                self.assertIn(
                    '"ortho":"","egib":"","landClasses":"","addresses":"","power":"","water":"","sewer":""',
                    first_fragment,
                )
                self.assertEqual(project["bbox"], metadata["spatial"]["bbox"])
                self.assertEqual(project["crs"], metadata["spatial"]["crs"])
                self.assertEqual(
                    project["plan"]["coordinateOrder"],
                    metadata["spatial"]["gmlCoordinateOrder"],
                )
                self.assertEqual(
                    project["wms130AxisOrder"],
                    metadata["spatial"]["wms130AxisOrder"],
                )

                parcels = build_map.load_parcels(project, map_dir / "sources" / "parcels")
                zones = build_map.load_plan_features(
                    project,
                    "StrefaPlanistyczna",
                    map_dir / "sources",
                )
                expected_parcels = 1 if fixture_name == "single-xy" else 2
                self.assertEqual(len(parcels["features"]), expected_parcels)
                self.assertEqual(len(zones["features"]), 1)
                first_zone_point = zones["features"][0]["geometry"]["coordinates"][0][0][0]
                self.assertGreaterEqual(first_zone_point[0], project["bbox"][0])
                self.assertGreaterEqual(first_zone_point[1], project["bbox"][1])


if __name__ == "__main__":
    unittest.main()
