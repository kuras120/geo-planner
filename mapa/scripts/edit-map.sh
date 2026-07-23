#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/build-map.sh"
exec python3 "$SCRIPT_DIR/edit_map_server.py" "$@"
