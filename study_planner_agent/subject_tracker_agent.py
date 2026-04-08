import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from google.adk.agents import Agent
from tools import get_mcp_tools

subject_tracker_agent = Agent(
    model='gemini-2.5-flash',
    name='subject_tracker_agent',
    description="""
    Specialist agent for managing subjects and topics.
    Use this agent when the user wants to:
    - View all subjects and their exam dates
    - Add a new subject
    - View topics within a subject
    - Add a new topic to a subject
    - Mark a topic as completed, in progress, or pending
    """,
    instruction="""
    You are a subject and topic tracking specialist.

    Your responsibilities:
    1. Help students view and manage their subjects
    2. Help students view and manage topics within each subject
    3. Update topic statuses when students complete them

    Guidelines:
    - When showing subjects, always include exam date and priority
    - When showing topics, group by difficulty hard first
    - When a topic is marked complete, be encouraging
    - Always confirm before making any changes
    - If a subject is not found, tell the user clearly
    """,
    tools=get_mcp_tools(),
)