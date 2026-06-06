#!/usr/bin/env bash
# Refresh the data.opengem.org snapshot.
#
# Intended to be run from a Dagster sensor or a daily cron — produces a fresh
# SQLite snapshot of the current vintage and pushes it onto the Fly volume.
#
# Required env:
#   FLY_APP — the Fly app name (default: opengem-data)
#   OPENGEM_VINTAGE_DSN — the source DSN (used by opengem-vintage if not 'demo')
#
# Usage:
#   ./snapshot-refresh.sh                  # uses today's vintage
#   ./snapshot-refresh.sh 2026-06-06       # specific vintage
#   ./snapshot-refresh.sh demo             # bundled fixture demo

set -euo pipefail

FLY_APP="${FLY_APP:-opengem-data}"
VINTAGE="${1:-today}"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

echo "[1/3] writing snapshot for vintage=$VINTAGE"
opengem-snapshot --vintage "$VINTAGE" --out "$WORKDIR/opengem.db" \
    --metadata "$WORKDIR/metadata.yaml"

echo "[2/3] uploading to fly volume on $FLY_APP"
fly ssh sftp shell -a "$FLY_APP" <<EOF
put $WORKDIR/opengem.db /data/opengem.db.new
put $WORKDIR/metadata.yaml /data/metadata.yaml.new
EOF

echo "[3/3] atomic swap via ssh"
fly ssh console -a "$FLY_APP" -C "mv /data/opengem.db.new /data/opengem.db && mv /data/metadata.yaml.new /data/metadata.yaml && systemctl restart datasette 2>/dev/null || true"

echo "OK — data.opengem.org refreshed at $(date -u +%FT%TZ)"
