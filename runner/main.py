# runner/main.py

import os
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.apps.app import App, ResumabilityConfig
from google.genai import types

# --- 1. CONFIGURATION ---
APP_NAME = "scholarship_orchestrator_app"
USER_ID = "default"
DB_URL = "sqlite:///scholarship_orchestrator.db"
MODEL_NAME = "gemini-2.5-flash-lite"
# Ensure GOOGLE_API_KEY is set in your environment variables for local testing
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"

# Clean up old database files for a fresh start if needed
if os.path.exists(DB_URL.replace("sqlite:///", "")):
    os.remove(DB_URL.replace("sqlite:///", ""))
    print(f"✅ Cleaned up old database file: {DB_URL.replace('sqlite:///', '')}")

# --- 2. IMPORT AGENT ---
# The Orchestrator agent should be imported from the agents package
from agents.orchestrator import orchestrator_agent


# --- 3. HELPER FUNCTION (From Notebook) ---
# Note: This function requires 'session_service' to be defined later.
async def run_session(
        runner_instance: Runner,
        user_queries: list[str] | str = None,
        session_name: str = "default",
):
    print(f"\n ### Session: {session_name}")

    app_name = runner_instance.app_name

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


# --- 4. SERVICES AND RUNNER SETUP ---

# Initialize Session Service (Persistent)
session_service = DatabaseSessionService(db_url=DB_URL)

# Initialize Memory Service (In-memory, for now)
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

print("✅ Orchestrator Runner initialized successfully!")


# --- 5. MAIN EXECUTION BLOCK ---
async def main():
    """Runs a comprehensive test workflow for the Scholarship Orchestrator."""

    session_id = "full-workflow-test-01"

    print("\n--- 📝 Step 1: User Profile and Application Input ---")

    # First run: Saving name and application-related data
    await run_session(
        orchestrator_runner,
        [
            "My name is Rifat Hasan. I am from Bangladesh.",
            "I have an MBA and I want to apply for a PhD in Management."
        ],
        session_id
    )

    print("\n--- 🔎 Step 2: Finding Scholarships (Triggering Tools/Finder) ---")

    # Second run: Finding scholarships using saved data
    await run_session(
        orchestrator_runner,
        [
            "Can you find 5 fully-funded PhD scholarships for Management in the USA or UK?"
        ],
        session_id
    )

    print("\n--- ✍️ Step 3: SOP Generation and HITL (Orchestration Pipeline) ---")

    # Third run: Triggering SOP generation and refinement pipeline
    await run_session(
        orchestrator_runner,
        [
            "Using my profile, please write an excellent Statement of Purpose (SOP) for a PhD at Oxford University. Focus on my research experience."
        ],
        session_id
    )

    # The HITL tool will PAUSE here.
    # If we run this in a real scenario, the Human Reviewer's decision must be input in the subsequent prompt.
    # E.g.: "The SOP draft is approved."

    print("\n✅ Request sent to test all main functionalities (Save, Find, Generate).")
    print("Next step: Continue the session by responding to the HITL (Human-in-the-Loop) request in your environment.")


if __name__ == "__main__":
    # Ensure all asynchronous components are run
    asyncio.run(main())