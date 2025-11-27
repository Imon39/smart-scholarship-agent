# test/test_workflow.py
# This file serves as the dedicated entry point for testing the full multi-agent workflow.

import os
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.apps.app import App, ResumabilityConfig
from google.genai import types

# --- 1. CONFIGURATION ---
APP_NAME = "scholarship_orchestrator_app"
USER_ID = "test_user"  # Using a dedicated ID for testing
DB_URL = "sqlite:///test_workflow_data.db"  # Using a separate DB file for testing
MODEL_NAME = "gemini-2.5-flash-lite"

# Clean up old database files for a fresh start (Crucial for reproducible tests)
if os.path.exists(DB_URL.replace("sqlite:///", "")):
    os.remove(DB_URL.replace("sqlite:///", ""))
    print(f"✅ Cleaned up old test database file: {DB_URL.replace('sqlite:///', '')}")

# --- 2. IMPORT AGENT ---
# The orchestrator is the root agent of the application
from agents.orchestrator import orchestrator_agent


# --- 3. HELPER FUNCTION: run_session (The core testing utility) ---
async def run_session(
        runner_instance: Runner,
        user_queries: list[str] | str = None,
        session_name: str = "default",
):
    print(f"\n ### Session: {session_name}")

    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one (for multi-turn tests)
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )

    if user_queries:
        if type(user_queries) == str:
            user_queries = [user_queries]

        for query in user_queries:
            print(f"\nUser > {query}")
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response
            async for event in runner_instance.run_async(
                    user_id=USER_ID, session_id=session.id, new_message=query
            ):
                if event.content and event.content.parts:
                    if (
                            event.content.parts[0].text != "None"
                            and event.content.parts[0].text
                    ):
                        print(f"{MODEL_NAME} > ", event.content.parts[0].text)
    else:
        print("No queries!")


# --- 4. SERVICES AND RUNNER SETUP (Local setup for the test file) ---

# Initialize Session Service (Using a test-specific DB)
session_service = DatabaseSessionService(db_url=DB_URL)

# Initialize Memory Service
memory_service = InMemoryMemoryService()

# Wrap Orchestrator in a resumable App
orchestrator_app = App(
    name=APP_NAME,
    root_agent=orchestrator_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

# Initialize the Runner
orchestrator_runner = Runner(
    app=orchestrator_app,
    session_service=session_service,
    memory_service=memory_service,
)

print("✅ Orchestrator Runner initialized successfully for testing!")


# --- 5. MAIN EXECUTION BLOCK (The Evaluation Workflow from the Notebook) ---
async def main():
    """Runs a comprehensive test workflow covering Save, Find, and Generate/HITL functionalities."""

    session_id = "test-session-full-cycle"

    print("\n--- 📝 Test Step 1: Saving User Profile (save_userinfo) ---")

    await run_session(
        orchestrator_runner,
        [
            "My name is Rifat Hasan. I am from Bangladesh.",
            "I have an MBA and I want to apply for a PhD in Management."
        ],
        session_id
    )

    print("\n--- 🔎 Test Step 2: Finding Scholarships (scholarship_agent & finder) ---")

    await run_session(
        orchestrator_runner,
        [
            "Can you find 5 fully-funded PhD scholarships for Management in the USA or UK?"
        ],
        session_id
    )

    print("\n--- ✍️ Test Step 3: Document Generation & HITL (Full Orchestration Pipeline) ---")

    await run_session(
        orchestrator_runner,
        [
            "Using my saved profile, please write an excellent Statement of Purpose (SOP) for a PhD at Oxford University. Focus on my research experience."
        ],
        session_id
    )

    # After Step 3, the execution will pause due to the HITL tool, awaiting a human decision.


if __name__ == "__main__":
    # Ensure all asynchronous components are run
    asyncio.run(main())