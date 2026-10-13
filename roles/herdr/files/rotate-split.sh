#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${HERDR_BIN_PATH:-}" && -x "${HERDR_BIN_PATH}" ]]; then
    HERDR_BIN="${HERDR_BIN_PATH}"
elif PATH="$HOME/.local/bin:$PATH" command -v herdr > /dev/null 2>&1; then
    HERDR_BIN="$(PATH="$HOME/.local/bin:$PATH" command -v herdr)"
else
    HERDR_BIN="$HOME/.local/bin/herdr"
fi

PANE_ID="${HERDR_ACTIVE_PANE_ID:-${HERDR_PANE_ID:-}}"

LAYOUT_ARGS=(pane layout)
if [[ -n "$PANE_ID" ]]; then
    LAYOUT_ARGS+=(--pane "$PANE_ID")
fi

LAYOUT_JSON="$("$HERDR_BIN" "${LAYOUT_ARGS[@]}" 2> /dev/null || true)"
[[ -n "$LAYOUT_JSON" ]] || exit 0

eval "$(python3 -c '
import json, sys
try:
    data = json.loads(sys.stdin.read())
    layout = data.get("result", {}).get("layout") or data.get("layout") or data
    panes = layout.get("panes", [])
    splits = layout.get("splits", [])
    if len(panes) < 2 or not splits or layout.get("zoomed"):
        sys.exit(0)
    tab_id = layout["tab_id"]
    focused = layout["focused_pane_id"]
    other = next((p["pane_id"] for p in panes if p["pane_id"] != focused), panes[0]["pane_id"])
    f_rect = next((p["rect"] for p in panes if p["pane_id"] == focused), panes[0]["rect"])
    o_rect = next((p["rect"] for p in panes if p["pane_id"] == other), panes[-1]["rect"])
    if abs(f_rect["y"] - o_rect["y"]) < abs(f_rect["x"] - o_rect["x"]):
        new_dir = "down"
    else:
        new_dir = "right"
    print(f"TAB_ID={tab_id!r}\nMOVING_PANE={focused!r}\nTARGET_PANE={other!r}\nNEW_DIR={new_dir!r}")
except Exception:
    pass
' <<< "$LAYOUT_JSON")"

[[ -n "${TAB_ID:-}" && -n "${MOVING_PANE:-}" && -n "${TARGET_PANE:-}" && -n "${NEW_DIR:-}" ]] || exit 0

MOVE_OUT="$("$HERDR_BIN" pane move "$MOVING_PANE" --new-tab --no-focus 2> /dev/null || true)"
NEW_PANE_ID="$(python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.read())
    res = d.get("result", d)
    print(res.get("pane", {}).get("pane_id", ""))
except Exception:
    pass
' <<< "$MOVE_OUT")"

MOVED_ID="${NEW_PANE_ID:-$MOVING_PANE}"
"$HERDR_BIN" pane move "$MOVED_ID" --tab "$TAB_ID" --target-pane "$TARGET_PANE" --split "$NEW_DIR" --ratio 0.5 --focus > /dev/null 2>&1 || true
