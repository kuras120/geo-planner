from __future__ import annotations

import base64
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

MAP_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = MAP_DIR / "sources"
PARCEL_DIR = SOURCE_DIR / "parcels"
PROJECT_CONFIG = MAP_DIR / "project-config.json"
MAP_CONFIG = MAP_DIR / "map-config.json"
TEMPLATE = MAP_DIR / "map-fragment.template.html"
FRAGMENT_OUTPUT = MAP_DIR / "map-fragment.html"
MANUAL_OVERLAYS = MAP_DIR / "manual-overlays.json"
MANUAL_OVERLAYS_EXAMPLE = MAP_DIR / "manual-overlays.example.json"

GML_NS = "http://www.opengis.net/gml/3.2"
SAFE_FILE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} musi zawierać obiekt JSON.")
    return value


def load_or_create_manual_overlays() -> dict[str, Any]:
    """Load local user overlays, creating an empty private file on first run."""
    if MANUAL_OVERLAYS.exists():
        return load_json(MANUAL_OVERLAYS)

    initial = load_json(MANUAL_OVERLAYS_EXAMPLE)
    encoded = json.dumps(initial, ensure_ascii=False, indent=2) + "\n"
    try:
        with MANUAL_OVERLAYS.open("x", encoding="utf-8") as overlays_file:
            overlays_file.write(encoded)
    except FileExistsError:
        pass
    return load_json(MANUAL_OVERLAYS)


def validate_project_config(config: dict[str, Any]) -> dict[str, Any]:
    required_strings = ("projectId", "title", "description", "outputFile", "locale", "crs", "precinctId")
    for key in required_strings:
        if not isinstance(config.get(key), str) or not config[key].strip():
            raise ValueError(f"project-config.json: pole {key} musi być niepustym tekstem.")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", config["projectId"]):
        raise ValueError("project-config.json: projectId musi mieć format lowercase-kebab-case.")
    if not SAFE_FILE.fullmatch(config["outputFile"]) or not config["outputFile"].endswith(".html"):
        raise ValueError("project-config.json: outputFile musi być bezpieczną nazwą pliku HTML.")
    bbox = config.get("bbox")
    if not isinstance(bbox, list) or len(bbox) != 4 or not all(isinstance(value, (int, float)) for value in bbox):
        raise ValueError("project-config.json: bbox musi zawierać cztery liczby.")
    if not (bbox[0] < bbox[2] and bbox[1] < bbox[3]):
        raise ValueError("project-config.json: bbox musi mieć kolejność minX, minY, maxX, maxY.")
    if config.get("wms130AxisOrder") not in {"xy", "yx"}:
        raise ValueError("project-config.json: wms130AxisOrder musi mieć wartość xy albo yx.")
    plan = config.get("plan")
    if not isinstance(plan, dict) or not SAFE_FILE.fullmatch(str(plan.get("file", ""))):
        raise ValueError("project-config.json: plan.file musi być bezpieczną nazwą pliku.")
    if not isinstance(plan.get("url"), str) or not plan["url"].startswith("https://"):
        raise ValueError("project-config.json: plan.url musi być adresem HTTPS.")
    if plan.get("coordinateOrder") not in {"xy", "yx"}:
        raise ValueError("project-config.json: plan.coordinateOrder musi mieć wartość xy albo yx.")
    parcels = config.get("parcels")
    if not isinstance(parcels, list) or not parcels:
        raise ValueError("project-config.json: parcels musi być niepustą listą.")
    numbers: set[str] = set()
    files: set[str] = set()
    for index, parcel in enumerate(parcels):
        if not isinstance(parcel, dict) or not isinstance(parcel.get("number"), str):
            raise ValueError(f"project-config.json: parcels[{index}] wymaga pola number.")
        file_name = parcel.get("file")
        if not isinstance(file_name, str) or not SAFE_FILE.fullmatch(file_name):
            raise ValueError(f"project-config.json: parcels[{index}].file ma nieprawidłową nazwę.")
        if parcel["number"] in numbers or file_name in files:
            raise ValueError("project-config.json: numery i pliki działek muszą być unikalne.")
        numbers.add(parcel["number"])
        files.add(file_name)
    rasters = config.get("rasters")
    if not isinstance(rasters, dict):
        raise ValueError("project-config.json: rasters musi być obiektem.")
    required_rasters = {"ortho", "egib", "addresses", "power", "water", "sewer"}
    if not required_rasters.issubset(rasters):
        raise ValueError("project-config.json: brakuje jednej ze standardowych warstw rastra.")
    for key, relative_path in rasters.items():
        path = Path(str(relative_path))
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"project-config.json: raster {key} musi wskazywać plik wewnątrz katalogu mapy.")
    services = config.get("services")
    required_services = {"uldk", "ortho", "egib", "utilities", "addresses"}
    if not isinstance(services, dict) or not required_services.issubset(services):
        raise ValueError("project-config.json: brakuje jednej ze standardowych usług źródłowych.")
    if not all(isinstance(services[key], str) and services[key].startswith("https://") for key in required_services):
        raise ValueError("project-config.json: adresy usług muszą używać HTTPS.")
    raster_size = config.get("rasterSize")
    if not isinstance(raster_size, dict) or not all(isinstance(raster_size.get(key), int) and raster_size[key] > 0 for key in ("width", "height")):
        raise ValueError("project-config.json: rasterSize wymaga dodatnich width i height.")
    return config


def split_top_level(text: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    start = 0
    for index, character in enumerate(text):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def parse_ring(text: str) -> list[list[float]]:
    return [[float(value) for value in pair.strip().split()[:2]] for pair in text.split(",")]


def parse_polygon_body(body: str) -> list[list[list[float]]]:
    inner = body.strip()[1:-1]
    return [parse_ring(ring.strip()[1:-1]) for ring in split_top_level(inner)]


def parse_wkt(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if len(lines) < 2:
        raise ValueError("Odpowiedź ULDK nie zawiera geometrii.")
    value = lines[1].split("|", 1)[0].strip()
    value = re.sub(r"^SRID=\d+;", "", value, flags=re.IGNORECASE)
    match = re.fullmatch(r"(POLYGON|MULTIPOLYGON)\s*(\(.+\))", value, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"Nieobsługiwany WKT: {value[:60]}")
    geometry_type = match.group(1).upper()
    body = match.group(2)
    if geometry_type == "POLYGON":
        return {"type": "Polygon", "coordinates": parse_polygon_body(body)}
    polygons = [parse_polygon_body(part) for part in split_top_level(body[1:-1])]
    return {"type": "MultiPolygon", "coordinates": polygons}


def uldk_parcel_number(text: str) -> str:
    lines = text.splitlines()
    if len(lines) < 2:
        raise ValueError("Odpowiedź ULDK nie zawiera danych działki.")
    fields = lines[1].split("|")
    if len(fields) < 2 or not fields[-1].strip():
        raise ValueError("Odpowiedź ULDK nie zawiera numeru działki.")
    return fields[-1].strip()


def load_parcels(config: dict[str, Any]) -> dict[str, Any]:
    features = []
    for parcel in config["parcels"]:
        path = PARCEL_DIR / parcel["file"]
        if not path.exists():
            raise FileNotFoundError(f"Brak źródła działki {parcel['number']}: {path}")
        source_text = path.read_text(encoding="utf-8")
        source_number = uldk_parcel_number(source_text)
        if source_number != parcel["number"]:
            raise ValueError(f"Źródło {path.name} opisuje działkę {source_number}, oczekiwano {parcel['number']}.")
        properties = {
            "number": parcel["number"],
            "area_ha": parcel.get("areaHa"),
            "kind": parcel.get("kind", "context"),
            "status": parcel.get("status", "działka kontekstowa"),
            "zones": parcel.get("zones", {}),
        }
        features.append({"type": "Feature", "properties": properties, "geometry": parse_wkt(source_text)})
    return {"type": "FeatureCollection", "features": features}


def parse_pos_list(text: str, coordinate_order: str) -> list[list[float]]:
    values = [float(value) for value in text.split()]
    if len(values) % 2:
        raise ValueError("Lista współrzędnych GML ma nieparzystą liczbę wartości.")
    pairs = [[values[index], values[index + 1]] for index in range(0, len(values), 2)]
    return [[second, first] for first, second in pairs] if coordinate_order == "yx" else pairs


def intersects_bbox(rings: list[list[list[float]]], bbox: list[float]) -> bool:
    points = [point for ring in rings for point in ring]
    min_x, max_x = min(point[0] for point in points), max(point[0] for point in points)
    min_y, max_y = min(point[1] for point in points), max(point[1] for point in points)
    return not (max_x < bbox[0] or min_x > bbox[2] or max_y < bbox[1] or min_y > bbox[3])


def load_plan_features(config: dict[str, Any], tag_name: str) -> dict[str, Any]:
    plan = config["plan"]
    plan_path = SOURCE_DIR / plan["file"]
    if not plan_path.exists():
        raise FileNotFoundError(f"Brak źródła planu: {plan_path}")
    namespace = {"app": plan["schemaNamespace"], "gml": GML_NS}
    tree = ET.parse(plan_path)
    features = []
    for node in tree.findall(f".//app:{tag_name}", namespace):
        rings = [
            parse_pos_list(item.text, plan["coordinateOrder"])
            for item in node.findall(".//gml:posList", namespace)
            if item.text
        ]
        if not rings or not intersects_bbox(rings, config["bbox"]):
            continue
        designation = node.findtext("app:oznaczenie", default="", namespaces=namespace)
        symbol = node.findtext("app:symbol", default="", namespaces=namespace)
        features.append({
            "type": "Feature",
            "properties": {"designation": designation, "symbol": symbol or "OUZ"},
            "geometry": {"type": "MultiPolygon", "coordinates": [[ring] for ring in rings]},
        })
    return {"type": "FeatureCollection", "features": features}


def data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def replace_required(source: str, marker: str, value: Any) -> str:
    if marker not in source:
        raise ValueError(f"Szablon nie zawiera znacznika {marker}.")
    encoded = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return source.replace(marker, encoded)


def standalone_document(fragment: str, project: dict[str, Any]) -> str:
    title = project["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'''<!doctype html>
<html lang="{project["locale"].split("-")[0]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{ color-scheme: light dark; --background: light-dark(#ffffff,#151716); --foreground: light-dark(#17201a,#edf3ef); --card: light-dark(#ffffff,#1d211e); --card-foreground: var(--foreground); --muted: light-dark(#e9eee9,#293029); --muted-foreground: light-dark(#566159,#aeb9b1); --border: light-dark(#cdd6cf,#465047); --primary: light-dark(#1d6046,#8ac8a8); --primary-foreground: light-dark(#ffffff,#102118); --accent: light-dark(#dcebe2,#32463a); --accent-foreground: var(--foreground); --input: var(--border); --ring: var(--primary); --viz-series-1: light-dark(#176b4a,#67bc91); --viz-series-2: light-dark(#d4a72c,#e2c56a); --viz-series-3: light-dark(#5f8f68,#91bd96); --viz-series-4: light-dark(#5269a5,#90a5e0); --viz-series-5: light-dark(#a85d30,#df996e); --viz-series-6: light-dark(#9a4455,#d98c9b); font-family: ui-sans-serif,system-ui,sans-serif; }}
    body {{ margin: 0; padding: 18px; background: var(--background); color: var(--foreground); }}
    body.gp-standalone {{ box-sizing: border-box; height: 100vh; height: 100dvh; overflow: hidden; }}
    body.gp-standalone #geo-layer-map.clm-workspace, body.gp-standalone #geo-layer-map.clm-workspace .clm-layout {{ height: 100%; }}
    body.gp-standalone #geo-layer-map.clm-workspace .clm-map, body.gp-standalone #geo-layer-map.clm-workspace .clm-svg {{ height: 100%; min-height: 0; }}
    body.gp-standalone #geo-layer-map.clm-workspace .clm-sidebar {{ height: 100%; min-height: 0; overflow-y: auto; scrollbar-gutter: stable; padding-inline-end: 8px; }}
    @media (max-width: 760px) {{ body.gp-standalone {{ height: auto; min-height: 100vh; overflow: auto; }} body.gp-standalone #geo-layer-map.clm-workspace, body.gp-standalone #geo-layer-map.clm-workspace .clm-layout {{ height: auto; }} body.gp-standalone #geo-layer-map.clm-workspace .clm-map, body.gp-standalone #geo-layer-map.clm-workspace .clm-svg {{ height: auto; min-height: var(--clm-mobile-min-height); }} body.gp-standalone #geo-layer-map.clm-workspace .clm-sidebar {{ height: auto; overflow: visible; padding-inline-end: 0; }} }}
    .card {{ background: var(--card); color: var(--card-foreground); border: 1px solid var(--border); border-radius: 12px; }}
    .btn,.form-control,.form-select {{ font: inherit; color: var(--foreground); background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 7px 10px; }}
    .btn {{ cursor: pointer; }} .btn:hover {{ border-color: var(--primary); }} .btn:focus-visible,.form-control:focus-visible,.form-select:focus-visible {{ outline: 2px solid var(--ring); outline-offset: 2px; }}
    .viz-controls {{ display: flex; flex-wrap: wrap; gap: 7px; }} .form-label {{ display: grid; gap: 5px; }} .form-check {{ display: flex; align-items: center; gap: 7px; }} .text-small {{ font-size: .84rem; }} .text-muted {{ color: var(--muted-foreground); }}
  </style>
</head>
<body class="gp-standalone">
<script>
  (() => {{
    if (location.protocol !== "http:" || !new Set(["127.0.0.1", "localhost", "::1"]).has(location.hostname)) return;
    let knownBuildVersion = null;
    window.geoPlannerSaveManual = async collection => {{
      const response = await fetch("/api/manual-overlays", {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify(collection) }});
      if (!response.ok) throw new Error((await response.text()) || `HTTP ${{response.status}}`);
      const result = await response.json(); knownBuildVersion = result.version || knownBuildVersion; return result;
    }};
    const checkBuildVersion = async () => {{ try {{ const response = await fetch("/api/build-version", {{ cache: "no-store" }}); if (!response.ok) return; const result = await response.json(); if (knownBuildVersion === null) knownBuildVersion = result.version; else if (result.version !== knownBuildVersion) location.reload(); }} catch {{}} }};
    checkBuildVersion(); window.setInterval(checkBuildVersion, 1500);
  }})();
</script>
{fragment}</body>
</html>
'''


def build() -> tuple[Path, Path]:
    project = validate_project_config(load_json(PROJECT_CONFIG))
    output = MAP_DIR / project["outputFile"]
    map_data = {
        "bbox": project["bbox"], "crs": project["crs"], "plan_date": project["plan"]["date"],
        "parcels": load_parcels(project),
        "zones": load_plan_features(project, "StrefaPlanistyczna"),
        "ouz": load_plan_features(project, "ObszarUzupelnieniaZabudowy"),
    }
    rasters = {key: data_uri(MAP_DIR / relative_path) for key, relative_path in project["rasters"].items()}
    fragment = TEMPLATE.read_text(encoding="utf-8")
    for marker, value in (
        ("__PROJECT_CONFIG__", project), ("__MAP_DATA__", map_data), ("__RASTER_DATA__", rasters),
        ("__MANUAL_DATA__", load_or_create_manual_overlays()), ("__MAP_CONFIG__", load_json(MAP_CONFIG)),
    ):
        fragment = replace_required(fragment, marker, value)
    FRAGMENT_OUTPUT.write_text(fragment, encoding="utf-8")
    output.write_text(standalone_document(fragment, project), encoding="utf-8")
    return FRAGMENT_OUTPUT, output


def main() -> None:
    fragment, standalone = build()
    print(f"Zapisano {fragment} ({fragment.stat().st_size / 1024:.0f} KiB)")
    print(f"Zapisano {standalone} ({standalone.stat().st_size / 1024:.0f} KiB)")


if __name__ == "__main__":
    main()
