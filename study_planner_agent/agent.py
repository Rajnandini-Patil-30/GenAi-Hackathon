import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))

from google.adk.agents import Agent
from subject_tracker_agent import subject_tracker_agent
from schedule_builder_agent import schedule_builder_agent
from progress_monitor_agent import progress_monitor_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='study_planner_root',
    description='Primary coordinator agent for the student study planner system.',
    instruction="""
    You are the main coordinator of a smart study planning system.
    Today's date is: """ + str(date.today()) + """

    You have three specialist agents working under you:

    1. subject_tracker_agent
       - Managing subjects and exam dates via MCP Toolbox
       - Viewing and updating topics in AlloyDB
       - Adding new subjects or topics

    2. schedule_builder_agent
       - Building study schedules and plans via MCP Toolbox
       - Creating REAL events on Google Calendar via MCP
       - Logging study sessions and managing tasks

    3. progress_monitor_agent
       - Tracking overall study progress via MCP Toolbox
       - Sending progress reports via Gmail MCP
       - Giving recommendations and motivational coaching

    Routing guide:
    - show subjects / add subject / topics → subject_tracker_agent
    - study plan / schedule / tasks / log session / calendar → schedule_builder_agent
    - progress / how am I doing / send email / recommendations → progress_monitor_agent

    Always greet new users warmly and ask how you can help.
    Be encouraging — exams are stressful and students need support!
    """,
    sub_agents=[
        subject_tracker_agent,
        schedule_builder_agent,
        progress_monitor_agent,
    ],
)