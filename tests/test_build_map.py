from __future__ import annotations

import copy
import contextlib
import io
import json
import re
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

    def test_land_classification_raster_is_configured(self) -> None:
        self.assertEqual(self.config["rasters"]["landClasses"], "assets/egib-land-use-classes.png")
        parameters = dict(update_sources.wms_parameters(self.config, "uzytki,kontury"))
        self.assertEqual(parameters["LAYERS"], "uzytki,kontury")
        self.assertEqual(parameters["CRS"], "EPSG:2178")
        self.assertEqual(parameters["FORMAT"], "image/png")
        self.assertEqual(parameters["TRANSPARENT"], "TRUE")

    def test_wms_dimensions_are_fixed_config_values_independent_of_bbox(self) -> None:
        parameters = dict(update_sources.wms_parameters(self.config, "Raster"))
        self.assertEqual(parameters["WIDTH"], str(self.config["rasterSize"]["width"]))
        self.assertEqual(parameters["HEIGHT"], str(self.config["rasterSize"]["height"]))

        larger_bbox = copy.deepcopy(self.config)
        larger_bbox["bbox"] = [
            self.config["bbox"][0],
            self.config["bbox"][1],
            self.config["bbox"][2] + 5000,
            self.config["bbox"][3] + 5000,
        ]
        larger_parameters = dict(update_sources.wms_parameters(larger_bbox, "Raster"))
        self.assertEqual(larger_parameters["WIDTH"], parameters["WIDTH"])
        self.assertEqual(larger_parameters["HEIGHT"], parameters["HEIGHT"])


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
    def setUp(self) -> None:
        self.config = json.loads((ROOT / "mapa" / "project-config.json").read_text(encoding="utf-8"))

    def test_failed_optional_download_preserves_existing_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "optional.png"
            output.write_bytes(b"previous snapshot")
            with mock.patch.object(update_sources.subprocess, "run", side_effect=CalledProcessError(22, "curl")):
                with contextlib.redirect_stdout(io.StringIO()):
                    update_sources.curl("https://example.invalid/layer", output, optional=True)
            self.assertEqual(output.read_bytes(), b"previous snapshot")
            self.assertEqual(list(Path(directory).iterdir()), [output])

    def test_refresh_requests_kieg_land_use_and_classification_layers(self) -> None:
        with (
            mock.patch.object(update_sources, "load_json", return_value=self.config),
            mock.patch.object(update_sources, "validate_project_config", return_value=self.config),
            mock.patch.object(update_sources, "curl") as curl,
        ):
            update_sources.main()

        expected_output = ROOT / "mapa" / self.config["rasters"]["landClasses"]
        matching_calls = [call for call in curl.call_args_list if call.args[1] == expected_output]
        self.assertEqual(len(matching_calls), 1)
        self.assertEqual(dict(matching_calls[0].args[2])["LAYERS"], "uzytki,kontury")

    def test_refresh_raster_contracts_and_optionality(self) -> None:
        with (
            mock.patch.object(update_sources, "load_json", return_value=self.config),
            mock.patch.object(update_sources, "validate_project_config", return_value=self.config),
            mock.patch.object(update_sources, "curl") as curl,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            update_sources.main()

        raster_calls = {
            call.args[1].name: (dict(call.args[2]), call.kwargs)
            for call in curl.call_args_list
            if len(call.args) == 3 and call.args[1].parent.name == "assets"
        }
        expected_layers = {
            "addresses-streets.png": "prg-adresy,prg-ulice,prg-place",
            "ortho.jpg": "Raster",
            "egib-buildings.png": "budynki,numery_dzialek",
            "egib-land-use-classes.png": "uzytki,kontury",
            "przewod_elektroenergetyczny.png": "przewod_elektroenergetyczny",
            "przewod_wodociagowy.png": "przewod_wodociagowy",
            "przewod_kanalizacyjny.png": "przewod_kanalizacyjny",
        }
        self.assertEqual(
            {name: parameters["LAYERS"] for name, (parameters, _) in raster_calls.items()},
            expected_layers,
        )
        self.assertTrue(raster_calls["addresses-streets.png"][1]["optional"])
        self.assertTrue(all(
            not kwargs.get("optional", False)
            for name, (_, kwargs) in raster_calls.items()
            if name != "addresses-streets.png"
        ))
        self.assertEqual(raster_calls["addresses-streets.png"][0]["VERSION"], "1.1.1")
        self.assertEqual(raster_calls["ortho.jpg"][0]["FORMAT"], "image/jpeg")
        self.assertEqual(raster_calls["ortho.jpg"][0]["TRANSPARENT"], "FALSE")

    def test_refresh_resolves_every_configured_parcel_independently(self) -> None:
        with (
            mock.patch.object(update_sources, "load_json", return_value=self.config),
            mock.patch.object(update_sources, "validate_project_config", return_value=self.config),
            mock.patch.object(update_sources, "curl") as curl,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            update_sources.main()

        parcel_requests = [
            dict(call.args[2])
            for call in curl.call_args_list
            if len(call.args) == 3 and call.args[1].parent == update_sources.PARCEL_DIR
        ]
        self.assertEqual(
            [request["id"] for request in parcel_requests],
            [
                f"{self.config['precinctId']}.{parcel['number']}"
                for parcel in self.config["parcels"]
            ],
        )
        self.assertTrue(all(request["request"] == "GetParcelByIdOrNr" for request in parcel_requests))
        self.assertTrue(all(request["srid"] == "2178" for request in parcel_requests))


class MapTemplateTest(unittest.TestCase):
    def test_land_classification_layer_has_group_toggle_and_renderer(self) -> None:
        template = (ROOT / "mapa" / "map-fragment.template.html").read_text(encoding="utf-8")
        self.assertIn('data-layer-group="landClasses"', template)
        self.assertIn('data-raster-option="landClasses"', template)
        self.assertIn('data-layer="landClasses"', template)
        self.assertIn('"ortho", "egib", "landClasses", "addresses"', template)

    def test_layer_stack_sidebar_order_and_initial_visibility_are_characterized(self) -> None:
        template = (ROOT / "mapa" / "map-fragment.template.html").read_text(encoding="utf-8")
        config = json.loads((ROOT / "mapa" / "map-config.json").read_text(encoding="utf-8"))

        self.assertEqual(
            re.findall(r'data-layer-group="([^"]+)"', template),
            [
                "ortho", "zones", "ouz", "egib", "landClasses", "addresses",
                "power", "water", "sewer", "parcels", "manual", "draft", "labels",
            ],
        )
        sidebar_layers = re.findall(r'<input[^>]+data-layer="([^"]+)"', template)
        self.assertEqual(
            sidebar_layers,
            [
                "ortho", "parcels", "egib", "landClasses", "zones", "ouz",
                "addresses", "power", "water", "sewer", "manual",
            ],
        )
        self.assertEqual(set(config["initialLayers"]), set(sidebar_layers))

    def test_parcel_and_manual_selection_keyboard_contracts_are_characterized(self) -> None:
        template = (ROOT / "mapa" / "map-fragment.template.html").read_text(encoding="utf-8")

        self.assertIn('role: "button", tabindex: "0"', template)
        self.assertGreaterEqual(
            template.count('event.key === "Enter" || event.key === " "'),
            3,
        )
        self.assertIn('parcelLayer.checked = true;', template)
        self.assertIn('manualLayer.checked = true;', template)
        self.assertGreaterEqual(template.count('drawMode.value = "none";'), 2)
        self.assertIn('draftPoints = [];', template)


if __name__ == "__main__":
    unittest.main()
