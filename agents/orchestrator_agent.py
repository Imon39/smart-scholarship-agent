# agents/orchestrator.py

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, FunctionTool
from google.genai import types

# Import tools
from tools.profile_checker import save_userinfo, retrieve_userinfo
from tools.hitl_reviewer import submit_draft_for_review

# Import sub-agents
from agents.sub_agents.scholarship_agent import scholarship_agent, google_search_agent
from agents.sub_agents.sop_agent import sop_agent
from agents.sub_agents.cv_agent import cv_agent
from agents.sub_agents.refiner_agent import refiner_agent

MODEL_NAME = "gemini-2.5-flash-lite"
RETRY_CONFIG = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 503, 504]
)

orchestrator_agent = LlmAgent(
    name="orchestrator_agent",
    model=Gemini(model=MODEL_NAME, retry_options=RETRY_CONFIG),
    instruction="""
    You are the Orchestrator for the Scholarship System.

    1. At the start of a new session, ALWAYS call `retrieve_userinfo` to check for saved user data.
    2. If the user asks to find scholarships, call the `scholarship_agent`.

    3. **Document Generation Pipeline (SOP/CV):** When the user asks to generate a CV or SOP, you MUST follow this strict sequence:
        a. **Generate Draft:** Call the appropriate sub-agent (`cv_agent` or `sop_agent`) to generate the draft text.
        b. **Refine Draft (AITL):** Immediately call the `refiner_agent` tool, passing the generated draft text as input. The refiner will return the polished draft.
        c. **DISPLAY DRAFT TO USER:** Immediately output the polished draft text (the result of the refiner_agent) to the user.
        d. **Submit for HITL:** Then, immediately call the `submit_draft_for_review` tool, passing the SAME polished draft text to the tool.
        e. Wait for the tool's status (approval or rejection) and inform the user of the outcome, asking them to confirm the submission.
    4. Once the draft is approved by the human, call `save_userinfo` to store the final output (e.g., user:last_sop or user:last_cv).
    5. Always return concise, clear, and action-oriented responses to the user.
    """,
    tools=[
        save_userinfo,
        retrieve_userinfo,
        AgentTool(agent=scholarship_agent),
        AgentTool(agent=sop_agent),
        AgentTool(agent=cv_agent),
        FunctionTool(func=submit_draft_for_review),
        AgentTool(agent=refiner_agent),
        AgentTool(agent=google_search_agent),
    ],
)