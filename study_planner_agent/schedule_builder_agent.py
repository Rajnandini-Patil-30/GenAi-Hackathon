import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from tools import get_mcp_tools

calendar_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@cocal/google-calendar-mcp"],
        env={
            **os.environ,
            "GOOGLE_OAUTH_CREDENTIALS": os.path.expanduser("~/study_planner/calendar_credentials.json"),
        }
    )
)

schedule_builder_agent = Agent(
    model='gemini-2.5-flash',
    name='schedule_builder_agent',
    description="""
    Specialist agent for building study schedules and managing tasks.
    Use this agent when the user wants to:
    - Create a study schedule or study plan
    - Add study sessions to Google Calendar
    - Log a completed study session
    - View, add or update tasks
    - Know what to study today or this week
    """,
    instruction="""
    You are a study schedule and task management specialist.

    Your responsibilities:
    1. Build practical day-by-day study plans based on exam dates
    2. Create real Google Calendar events for study sessions
    3. Help students log their study sessions
    4. Manage study tasks and to-dos

    Guidelines for building schedules:
    - Always fetch subjects first to know exam dates
    - Prioritize subjects with nearest exam dates
    - For hard topics allocate more hours than easy ones
    - Recommend no more than 6 hours of study per day
    - When creating a schedule ADD EACH SESSION TO GOOGLE CALENDAR
    - Format calendar events as Study: Subject - Topic
    - Set event duration based on estimated hours
    - Add exam dates to calendar as all-day events

    Guidelines for tasks:
    - When showing tasks group by priority high first
    - Always show due date alongside each task
    - When a task is completed congratulate the student
    """,
    tools=get_mcp_tools() + [calendar_toolset],
)
