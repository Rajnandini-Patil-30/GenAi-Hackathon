import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from tools import get_mcp_tools

gmail_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="node",
        args=[
            "/usr/local/nvm/versions/node/v24.14.1/lib/node_modules/@gongrzhe/server-gmail-autoauth-mcp/dist/index.js"
        ],
        env={
            **os.environ,
            "NODE_ENV": "production",
            "DEBUG": "",
            "LOG_LEVEL": "error",
        }
    )
)

progress_monitor_agent = Agent(
    model='gemini-2.5-flash',
    name='progress_monitor_agent',
    description="""
    Specialist agent for tracking study progress and giving recommendations.
    Use this agent when the user wants to:
    - See their overall study progress
    - Get a progress report for a specific subject
    - Know which subjects need more attention
    - Get recommendations on what to focus on
    - Send progress report to email
    - Get motivational feedback on their progress
    """,
    instruction="""
    You are a study progress analyst and motivational coach.

    IMPORTANT: You have two sets of tools:
    1. Database tools (get_study_progress, get_all_subjects, etc.) - use these to fetch data
    2. Gmail tool (send_email) - use this to send emails directly

    NEVER write code. ALWAYS call tools directly.

    When asked to send a progress report:
    Step 1: Call get_study_progress to get the data
    Step 2: Format a clear plain text email body yourself
    Step 3: Call send_email directly with:
      - to: [the email address provided]
      - subject: "Study Progress Report - <today's date>"
      - body: your formatted progress summary

    Email format:
    - List each subject with completion % and exam date
    - Flag urgent subjects (below 50% complete)
    - Add a short motivational message at the end

    Progress indicators:
    - 0-30% = needs immediate attention
    - 31-60% = on track but needs consistency
    - 61-90% = doing well
    - 91-100% = excellent, focus on revision
    """,
    tools=get_mcp_tools() + [gmail_toolset],
)