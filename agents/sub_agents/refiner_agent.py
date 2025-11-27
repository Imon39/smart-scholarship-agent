# agents/refiner_agent.py

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

refiner_agent = LlmAgent(
    name="refiner_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""
    You are an academic editor.
    Your job is to take raw text and return:
    - grammatically correct
    - more concise
    - academic tone
    - logically structured
    Do NOT add new ideas. Only improve writing.
    """
)