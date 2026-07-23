from __future__ import annotations

import copy
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from subprocess import CalledProcessError
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mapa" / "scripts"))

import build_map  # noqa: E402
import update_sources  # noqa: E402


class ProjectConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads((ROOT / "mapa" / "project-config.json").read_text(encoding="utf-8"))

    def test_repository_config_is_valid(self) -> None:
        self.assertIs(build_map.validate_project_config(self.config), self.config)

    def test_duplicate_parcel_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.config)
        invalid["parcels"].append(copy.deepcopy(invalid["parcels"][0]))
        with self.assertRaisesRegex(ValueError, "unikalne"):
            build_map.validate_project_config(invalid)

    def test_output_path_cannot_escape_map_directory(self) -> None:
        invalid = copy.deepcopy(self.config)
        invalid["outputFile"] = "../outside.html"
        with self.assertRaisesRegex(ValueError, "outputFile"):
            build_map.validate_project_config(invalid)

    def test_wms_axis_order_uses_project_configuration(self) -> None:
        self.assertEqual(update_sources.wms_bbox(self.config), "5515080,7498460,5515600,7498940")
        xy = copy.deepcopy(self.config)
        xy["wms130AxisOrder"] = "xy"
        self.assertEqual(update_sources.wms_bbox(xy), "7498460,5515080,7498940,5515600")


class GeometryParsingTest(unittest.TestCase):
    def test_polygon_with_hole(self) -> None:
        geometry = build_map.parse_wkt("0\nPOLYGON ((0 0, 4 0, 4 4, 0 0), (1 1, 2 1, 1 1))|x")
        self.assertEqual(geometry["type"], "Polygon")
        self.assertEqual(len(geometry["coordinates"]), 2)

    def test_multipolygon(self) -> None:
        geometry = build_map.parse_wkt("0\nMULTIPOLYGON (((0 0, 1 0, 0 0)), ((2 2, 3 2, 2 2)))|x")
        self.assertEqual(geometry["type"], "MultiPolygon")
        self.assertEqual(len(geometry["coordinates"]), 2)

    def test_configurable_gml_coordinate_order(self) -> None:
        self.assertEqual(build_map.parse_pos_list("10 20 30 40", "xy"), [[10.0, 20.0], [30.0, 40.0]])
        self.assertEqual(build_map.parse_pos_list("10 20 30 40", "yx"), [[20.0, 10.0], [40.0, 30.0]])

    def test_uldk_parcel_number_comes_from_response(self) -> None:
        self.assertEqual(build_map.uldk_parcel_number("0\nPOLYGON ((0 0, 1 0, 0 0))|121601_4.0001.7/2|7/2"), "7/2")


class ManualOverlayLifecycleTest(unittest.TestCase):
    def test_missing_local_overlay_is_created_from_example(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            local_path = directory_path / "manual-overlays.json"
            example_path = directory_path / "manual-overlays.example.json"
            example = {"type": "FeatureCollection", "features": [], "instructions": "Local only"}
            example_path.write_text(json.dumps(example), encoding="utf-8")

            with (
                mock.patch.object(build_map, "MANUAL_OVERLAYS", local_path),
                mock.patch.object(build_map, "MANUAL_OVERLAYS_EXAMPLE", example_path),
            ):
                self.assertEqual(build_map.load_or_create_manual_overlays(), example)

            self.assertEqual(json.loads(local_path.read_text(encoding="utf-8")), example)

    def test_existing_local_overlay_is_never_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            local_path = directory_path / "manual-overlays.json"
            example_path = directory_path / "manual-overlays.example.json"
            existing = {"type": "FeatureCollection", "features": [{"type": "Feature"}]}
            local_path.write_text(json.dumps(existing), encoding="utf-8")
            example_path.write_text(json.dumps({"type": "FeatureCollection", "features": []}), encoding="utf-8")

            with (
                mock.patch.object(build_map, "MANUAL_OVERLAYS", local_path),
                mock.patch.object(build_map, "MANUAL_OVERLAYS_EXAMPLE", example_path),
            ):
                self.assertEqual(build_map.load_or_create_manual_overlays(), existing)

            self.assertEqual(json.loads(local_path.read_text(encoding="utf-8")), existing)


class SourceRefreshTest(unittest.TestCase):
    def test_failed_optional_download_preserves_existing_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "optional.png"
            output.write_bytes(b"previous snapshot")
            with mock.patch.object(update_sources.subprocess, "run", side_effect=CalledProcessError(22, "curl")):
                with contextlib.redirect_stdout(io.StringIO()):
                    update_sources.curl("https://example.invalid/layer", output, optional=True)
            self.assertEqual(output.read_bytes(), b"previous snapshot")
            self.assertEqual(list(Path(directory).iterdir()), [output])


if __name__ == "__main__":
    unittest.main()
