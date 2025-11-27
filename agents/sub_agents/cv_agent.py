# agents/cv_agent.py

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

cv_agent = LlmAgent(
    name="cv_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""
    You are an expert CV writer.
    1. Only generate a professional CV based on the user profile and scholarship details.
    2. Do NOT call any tools.
    3. Do NOT save anything. Just output the text of the CV.
    """
)