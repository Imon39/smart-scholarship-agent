"""
test_workflow.py"""

import asyncio
import os
from typing import List

# Import core ADK components
from google.genai import types
from google.adk.models.agent.runner import AgentRunner
from google.adk.models.agent.session import AgentSession
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.plugins.logging_plugin import LoggingPlugin

# Import your agent from your project
from agents.orchestrator_agent import scholarship_agent
from tools.scholarship_tool import find_scholarships


# -------------------------------
# 1. CONFIGURATION
# -------------------------------

APP_NAME = "scholarship_orchestrator_app"
USER_ID = "test_user"
MODEL_NAME = "gemini-2.5-flash-lite"
DB_URL = "sqlite:///test_workflow.db"


# -------------------------------
# 2. INITIALIZATION
# -------------------------------

# Persistent sessions
session_service = DatabaseSessionService(db_url=DB_URL)

# In-memory memory for development
memory_service = InMemoryMemoryService()

# Runner
runner = Runner(
    agent=scholarship_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service,
    plugins=[LoggingPlugin()],
)


# -------------------------------
# 3. Async Test Runner Helper
# -------------------------------

async def run_test_session(
    test_name: str,
    messages: List[str],
):
    print(f"\n\n============================")
    print(f" TEST: {test_name}")
    print(f"============================\n")

    # Ensure session exists
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=test_name
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=test_name
        )

    for msg in messages:
        print(f"\nUser > {msg}")
        message_obj = types.Content(role="user", parts=[types.Part(text=msg)])

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=message_obj
        ):
            if (
                event.content
                and event.content.parts
                and event.content.parts[0].text not in ("", "None")
            ):
                print(f"Agent > {event.content.parts[0].text}")


# -------------------------------
# 4. Test Cases
# -------------------------------

async def test_basic_flow():
    await run_test_session(
        "basic_flow",
        [
            "Hi, my name is Imon.",
            "I am from Bangladesh.",
            "I want a BSc level scholarship in any country with full funding.",
        ],
    )


async def test_missing_user_info():
    await run_test_session(
        "missing_info_flow",
        [
            "Find me scholarships for Masters.",
        ],
    )


async def test_no_match_scholarships():
    await run_test_session(
        "no_match_flow",
        [
            "I want a scholarship on Mars with $1 billion funding.",
        ],
    )


# -------------------------------
# 5. Run all tests when executed directly
# -------------------------------
if __name__ == "__main__":
    asyncio.run(test_basic_flow())
    asyncio.run(test_missing_user_info())
    asyncio.run(test_no_match_scholarships())

    print("\n\n✅ All test sessions completed.")
