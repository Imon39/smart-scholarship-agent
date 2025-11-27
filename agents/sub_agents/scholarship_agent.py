# agents/scholarship_agent.py

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search, AgentTool
from tools.finder import agent_scholarship_finder
from tools.profile_checker import save_userinfo, retrieve_userinfo
from google.genai import types # for HttpRetryOptions

# Global constants (usually better to pass via config, but fine for a module)
MODEL_NAME = "gemini-2.5-flash-lite"
RETRY_CONFIG = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# A Google Search Agent needs to be defined for the fallback search
google_search_agent = LlmAgent(
    name="google_search_scholarships", # Renamed for clarity inside the agent's tool list
    model=Gemini(model=MODEL_NAME, retry_options=RETRY_CONFIG),
    instruction="""Use google_search tool to find scholarships worldwide.\n    Return raw search results.\n    """,
    tools=[google_search]
)

scholarship_agent = LlmAgent(
    name="scholarship_agent",
    model=Gemini(model=MODEL_NAME, retry_options=RETRY_CONFIG),
    instruction="""
    You are a smart scholarship recommendation assistant.

--- Memory Rules ---
1. Whenever the user explicitly provides their name or country, you MUST call the `save_userinfo` tool to store it in session state using the `user:` prefix.
2. Before giving any scholarship recommendations, ALWAYS call the `retrieve_userinfo` tool to check whether user information is already stored.
3. If the user's name or country is missing after retrieval, politely ask the user for the missing details.

--- Scholarship Search Rules ---
4. When the user provides a scholarship query (degree, preferred country, funding preference), first call the `agent_scholarship_finder` tool.
5. If the tool returns an empty list, you MUST call the `Google Search_scholarships` tool as a fallback to find external scholarship information.
6. If both searches return no results, politely inform the user.

--- Output Formatting Rules ---
7. Format the final scholarship results as a bulleted list.
8. For EACH scholarship, use EXACTLY this template:

   **[Title]**
   * **Degrees**: [List of degrees]
   * **Funds**: [Funding amount]
   * **Country**: [Country]
   * **Deadline**: [Deadline]

9. If any information is missing, write "Not specified".
10. After the list, briefly explain WHY these scholarships match the user’s profile.""",
    tools=[
        agent_scholarship_finder, # Local finder tool
        save_userinfo,
        retrieve_userinfo,
        AgentTool(agent=google_search_agent) # External search agent as a tool
    ]
)