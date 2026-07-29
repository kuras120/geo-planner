from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mapa" / "scripts"))

import edit_map_server  # noqa: E402


class ManualOverlayValidationTest(unittest.TestCase):
    def test_supported_single_and_multi_geometries_round_trip_without_mutation(self) -> None:
        collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "multi-vertex path"},
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[0, 0], [1, 1], [2, 0]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"name": "area"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [2, 0], [1, 1], [0, 0]]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"name": "imported multipart"},
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [[[[0, 0], [1, 0], [0, 0]]]],
                    },
                },
            ],
        }

        self.assertIs(edit_map_server.validate_collection(collection), collection)

    def test_non_collection_and_unsupported_geometry_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "FeatureCollection"):
            edit_map_server.validate_collection({"type": "Feature"})

        with self.assertRaisesRegex(ValueError, "nieobsługiwaną geometrię"):
            edit_map_server.validate_collection({
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {},
                    "geometry": {"type": "GeometryCollection", "geometries": []},
                }],
            })

    def test_atomic_write_round_trips_collection_and_replaces_existing_file(self) -> None:
        collection = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {"name": "Łąka"},
                "geometry": {"type": "Point", "coordinates": [1, 2]},
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "manual-overlays.json"
            output.write_text('{"old": true}\n', encoding="utf-8")

            edit_map_server.write_collection_atomic(collection, output)

            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), collection)
            self.assertEqual(list(Path(directory).iterdir()), [output])

    def test_failed_atomic_replace_preserves_existing_file_and_removes_temporary_file(self) -> None:
        collection = {"type": "FeatureCollection", "features": []}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "manual-overlays.json"
            original = '{"type":"FeatureCollection","features":[{"old":true}]}\n'
            output.write_text(original, encoding="utf-8")

            with (
                mock.patch.object(edit_map_server.os, "replace", side_effect=OSError("replace failed")),
                self.assertRaisesRegex(OSError, "replace failed"),
            ):
                edit_map_server.write_collection_atomic(collection, output)

            self.assertEqual(output.read_text(encoding="utf-8"), original)
            self.assertEqual(list(Path(directory).iterdir()), [output])

    def test_persist_pipeline_validates_writes_then_forces_rebuild(self) -> None:
        collection = {"type": "FeatureCollection", "features": []}
        events = []

        with (
            mock.patch.object(
                edit_map_server,
                "write_collection_atomic",
                side_effect=lambda value: events.append(("write", value)),
            ),
            mock.patch.object(
                edit_map_server,
                "rebuild_if_needed",
                side_effect=lambda *, force: events.append(("rebuild", force)) or 123,
            ),
        ):
            persisted, version = edit_map_server.persist_collection(collection)

        self.assertIs(persisted, collection)
        self.assertEqual(version, 123)
        self.assertEqual(events, [("write", collection), ("rebuild", True)])

    def test_invalid_collection_does_not_write_or_rebuild(self) -> None:
        with (
            mock.patch.object(edit_map_server, "write_collection_atomic") as write,
            mock.patch.object(edit_map_server, "rebuild_if_needed") as rebuild,
            self.assertRaisesRegex(ValueError, "FeatureCollection"),
        ):
            edit_map_server.persist_collection({"type": "Feature"})

        write.assert_not_called()
        rebuild.assert_not_called()


if __name__ == "__main__":
    unittest.main()
