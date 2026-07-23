#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


MAP_DIR = Path(__file__).resolve().parents[1]
OVERLAYS = MAP_DIR / "manual-overlays.json"
OVERLAYS_EXAMPLE = MAP_DIR / "manual-overlays.example.json"
CONFIG = MAP_DIR / "map-config.json"
PROJECT_CONFIG = MAP_DIR / "project-config.json"
TEMPLATE = MAP_DIR / "map-fragment.template.html"
BUILD_SCRIPT = MAP_DIR / "scripts" / "build_map.py"
MAX_BODY = 5 * 1024 * 1024
BUILD_LOCK = threading.Lock()


def project_settings() -> dict:
    value = json.loads(PROJECT_CONFIG.read_text(encoding="utf-8"))
    output_file = value.get("outputFile")
    project_id = value.get("projectId")
    if not isinstance(output_file, str) or Path(output_file).name != output_file:
        raise ValueError("project-config.json zawiera nieprawidłowe outputFile.")
    if not isinstance(project_id, str) or not project_id:
        raise ValueError("project-config.json zawiera nieprawidłowe projectId.")
    return value


def standalone_path() -> Path:
    return MAP_DIR / project_settings()["outputFile"]


def build_inputs() -> list[Path]:
    paths = [OVERLAYS, OVERLAYS_EXAMPLE, CONFIG, PROJECT_CONFIG, TEMPLATE, BUILD_SCRIPT]
    for directory in (MAP_DIR / "sources", MAP_DIR / "assets"):
        if directory.exists():
            paths.extend(path for path in directory.rglob("*") if path.is_file())
    return paths


def rebuild_if_needed(*, force: bool = False) -> int:
    with BUILD_LOCK:
        standalone = standalone_path()
        overlays_missing = not OVERLAYS.exists()
        newest_input = max((path.stat().st_mtime_ns for path in build_inputs() if path.exists()), default=0)
        output_time = standalone.stat().st_mtime_ns if standalone.exists() else 0
        if force or overlays_missing or newest_input > output_time:
            subprocess.run(
                [sys.executable, str(BUILD_SCRIPT)],
                cwd=MAP_DIR,
                check=True,
                capture_output=True,
                text=True,
            )
        return standalone.stat().st_mtime_ns


def validate_collection(value: object) -> dict:
    if not isinstance(value, dict) or value.get("type") != "FeatureCollection":
        raise ValueError("Oczekiwano GeoJSON FeatureCollection.")
    features = value.get("features")
    if not isinstance(features, list):
        raise ValueError("Pole features musi być listą.")
    for index, feature in enumerate(features):
        if not isinstance(feature, dict) or feature.get("type") != "Feature":
            raise ValueError(f"Element features[{index}] nie jest GeoJSON Feature.")
        geometry = feature.get("geometry")
        if not isinstance(geometry, dict) or geometry.get("type") not in {
            "Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"
        }:
            raise ValueError(f"Element features[{index}] ma nieobsługiwaną geometrię.")
    return value


class MapHandler(SimpleHTTPRequestHandler):
    server_version = "GeoPlannerMapEditor/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(MAP_DIR), **kwargs)

    def end_headers(self) -> None:
        if self.path.endswith(".html") or self.path.startswith("/api/"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_json(self, status: int, value: dict) -> None:
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/build-version":
            super().do_GET()
            return
        try:
            version = rebuild_if_needed()
        except (OSError, subprocess.CalledProcessError) as error:
            self.send_json(500, {"ok": False, "error": str(error)})
            return
        self.send_json(200, {"ok": True, "version": version})

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/manual-overlays":
            self.send_error(404)
            return

        origin = self.headers.get("Origin")
        allowed_origins = {
            f"http://127.0.0.1:{self.server.server_port}",
            f"http://localhost:{self.server.server_port}",
        }
        if origin and origin not in allowed_origins:
            self.send_error(403, "Niedozwolone źródło żądania.")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                raise ValueError("Nieprawidłowy rozmiar danych.")
            collection = validate_collection(json.loads(self.rfile.read(length)))
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=MAP_DIR, prefix=".manual-overlays-", delete=False
            ) as temporary:
                json.dump(collection, temporary, ensure_ascii=False, indent=2)
                temporary.write("\n")
                temporary_path = Path(temporary.name)
            os.replace(temporary_path, OVERLAYS)
            version = rebuild_if_needed(force=True)
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as error:
            self.send_error(400, str(error))
            return
        except (OSError, subprocess.CalledProcessError) as error:
            self.send_json(500, {"ok": False, "error": str(error)})
            return

        self.send_json(200, {"ok": True, "features": len(collection["features"]), "version": version})


def main() -> None:
    parser = argparse.ArgumentParser(description="Lokalny edytor warstwy manual-overlays.json")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), MapHandler)
    output_file = project_settings()["outputFile"]
    print(f"Edytor mapy: http://127.0.0.1:{args.port}/{output_file}")
    print("Zakończ serwer skrótem Ctrl+C.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
