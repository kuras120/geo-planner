#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 -m unittest discover -s "$ROOT_DIR/tests" -p 'test_*.py'
python3 -m py_compile \
  "$ROOT_DIR/mapa/scripts/build_map.py" \
  "$ROOT_DIR/mapa/scripts/update_sources.py" \
  "$ROOT_DIR/mapa/scripts/edit_map_server.py"
python3 "$ROOT_DIR/mapa/scripts/build_map.py"

if rg -n '__[A-Z][A-Z_]+__' "$ROOT_DIR/mapa/map-fragment.html"; then
  echo "Wygenerowana mapa zawiera nierozwiązane znaczniki szablonu." >&2
  exit 1
fi

echo "Weryfikacja zakończona powodzeniem."
