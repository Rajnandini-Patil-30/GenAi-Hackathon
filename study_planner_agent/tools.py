import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from toolbox_core import ToolboxSyncClient

# Connect to MCP Toolbox server running on port 5001
toolbox = ToolboxSyncClient("http://127.0.0.1:5001")

def get_mcp_tools():
    return toolbox.load_toolset('study_planner_toolset')