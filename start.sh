#!/bin/bash
set -e

echo "=== Starting MCP Toolbox ==="
/app/toolbox --tools-file="/app/tools.yaml" --port=5001 &

echo "=== Waiting for MCP Toolbox (up to 60s) ==="
for i in {1..30}; do
    if curl -sf http://127.0.0.1:5001/api/toolset/study_planner_toolset > /dev/null 2>&1; then
        echo "MCP Toolbox ready after ${i}x2s!"
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 2
done

echo "=== Starting ADK web server ==="
exec adk web \
    --host=0.0.0.0 \
    --port=8080 \
    --allow_origins="*" \
    /app