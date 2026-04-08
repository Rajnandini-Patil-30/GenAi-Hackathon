import os
import sys
import uuid
from datetime import date
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Add agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'study_planner_agent'))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from google.genai.types import Content, Part

# Import the root agent
from study_planner_agent.agent import root_agent

# ─── FastAPI App ──────────────────────────────────────────────
app = FastAPI(
    title="Study Planner AI API",
    description="Multi-agent AI system to help students manage study plans",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Session Management ───────────────────────────────────────
session_service = InMemorySessionService()
APP_NAME = "study_planner"

# ─── Request/Response Models ──────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# ─── Routes ───────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status": "running",
        "app": "Study Planner AI",
        "version": "1.0.0",
        "today": str(date.today())
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Create or reuse session
        session_id = request.session_id or str(uuid.uuid4())
        user_id = "student"

        # Get or create session
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )
        if session is None:
            session = await session_service.create_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id
            )

        # Create runner
        runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )

        # Build message
        content = Content(
            role="user",
            parts=[Part(text=request.message)]
        )

        # Run agent and collect response
        final_response = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                break

        if not final_response:
            final_response = "I'm sorry, I couldn't process that request. Please try again."

        return ChatResponse(
            response=final_response,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/subjects")
async def get_subjects():
    """Quick endpoint to get all subjects directly."""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'study_planner_agent'))
        from tools import get_all_subjects
        return {"subjects": get_all_subjects()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/progress")
async def get_progress():
    """Quick endpoint to get study progress directly."""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'study_planner_agent'))
        from tools import get_study_progress
        return {"progress": get_study_progress()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks")
async def get_tasks():
    """Quick endpoint to get all tasks directly."""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'study_planner_agent'))
        from tools import get_all_tasks
        return {"tasks": get_all_tasks()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))