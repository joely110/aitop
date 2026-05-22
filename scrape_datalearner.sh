#!/bin/bash
set -e

# Start trajectory
npx -y ruvector@0.2.25 hooks trajectory-begin --context "datalearner scrape all models" --agent "browser-extract"

# The rest of the logic would go here, but browser tools are MCP tools not bash commands
# We need to use them via the Claude Code MCP interface

echo "Trajectory started"
