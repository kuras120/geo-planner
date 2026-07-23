#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable

from build_map import MAP_DIR, PARCEL_DIR, SOURCE_DIR, load_json, validate_project_config


def curl(url: str, output: Path, parameters: Iterable[tuple[str, str]] = (), *, optional: bool = False) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = tempfile.NamedTemporaryFile(dir=output.parent, prefix=f".{output.name}-", delete=False)
    temporary.close()
    temporary_path = Path(temporary.name)
    command = ["curl", "--retry", "3" if optional else "5", "--retry-all-errors", "--retry-delay", "2", "-L", "--fail", "--silent", "--show-error"]
    if parameters:
        command.append("--get")
        for key, value in parameters:
            command.extend(("--data-urlencode", f"{key}={value}"))
    command.extend((url, "-o", str(temporary_path)))
    try:
        subprocess.run(command, check=True)
        os.replace(temporary_path, output)
    except subprocess.CalledProcessError:
        temporary_path.unlink(missing_ok=True)
        if optional:
            print(f"Ostrzeżenie: nie udało się odświeżyć opcjonalnej warstwy {output.name}.")
            return
        raise
    except OSError:
        temporary_path.unlink(missing_ok=True)
        raise


def wms_bbox(config: dict) -> str:
    min_x, min_y, max_x, max_y = config["bbox"]
    values = (min_y, min_x, max_y, max_x) if config["wms130AxisOrder"] == "yx" else (min_x, min_y, max_x, max_y)
    return ",".join(str(value) for value in values)


def wms_parameters(config: dict, layers: str, *, version: str = "1.3.0", transparent: bool = True) -> list[tuple[str, str]]:
    size = config["rasterSize"]
    parameters = [
        ("SERVICE", "WMS"), ("VERSION", version), ("REQUEST", "GetMap"), ("LAYERS", layers),
        ("STYLES", ""), ("WIDTH", str(size["width"])), ("HEIGHT", str(size["height"])),
        ("FORMAT", "image/png" if transparent else "image/jpeg"), ("TRANSPARENT", "TRUE" if transparent else "FALSE"),
    ]
    if version == "1.3.0":
        parameters.extend((("CRS", config["crs"]), ("BBOX", wms_bbox(config))))
    else:
        parameters.extend((("SRS", config["crs"]), ("BBOX", ",".join(str(value) for value in config["bbox"]))))
    return parameters


def main() -> None:
    config = validate_project_config(load_json(MAP_DIR / "project-config.json"))
    services = config["services"]
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    PARCEL_DIR.mkdir(parents=True, exist_ok=True)
    (MAP_DIR / "assets").mkdir(parents=True, exist_ok=True)

    curl(config["plan"]["url"], SOURCE_DIR / config["plan"]["file"])
    srid = config["crs"].split(":", 1)[-1]
    for parcel in config["parcels"]:
        curl(services["uldk"], PARCEL_DIR / parcel["file"], (
            ("request", "GetParcelByIdOrNr"),
            ("id", f"{config['precinctId']}.{parcel['number']}"),
            ("result", "geom_wkt,teryt,parcel"),
            ("srid", srid),
        ))

    rasters = config["rasters"]
    curl(services["addresses"], MAP_DIR / rasters["addresses"], wms_parameters(config, "prg-adresy,prg-ulice,prg-place", version="1.1.1"), optional=True)
    curl(services["ortho"], MAP_DIR / rasters["ortho"], wms_parameters(config, "Raster", transparent=False))
    curl(services["egib"], MAP_DIR / rasters["egib"], wms_parameters(config, "budynki,numery_dzialek"))
    for key, layer in (("power", "przewod_elektroenergetyczny"), ("water", "przewod_wodociagowy"), ("sewer", "przewod_kanalizacyjny")):
        curl(services["utilities"], MAP_DIR / rasters[key], wms_parameters(config, layer))
    print(f"Zaktualizowano źródła projektu {config['projectId']}.")


if __name__ == "__main__":
    main()
