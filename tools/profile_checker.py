# tools/profile_checker.py

from google.adk.tools import ToolContext


def save_userinfo(
        tool_context: ToolContext, **kwargs
) -> dict[str, any]:
    """
    Flexible tool to save ANY user information into session state.
    All keys are auto-prefixed with 'user:'.
    """
    # Store all passed keyword arguments
    for key, value in kwargs.items():
        namespaced_key = f"user:{key}"
        tool_context.state[namespaced_key] = value

    return {"status": "success", "saved_fields": list(kwargs.keys())}


def retrieve_userinfo(tool_context: ToolContext) -> dict[str, any]:
    """
    Flexible tool to retrieve ALL user-related info
    (keys starting with 'user:') from session state.
    Returns a clean dictionary without the prefix.
    """
    user_data = {}

    # Access the State object's combined dictionary safely
    # Note: In a live ADK environment, checking tool_context.state should be enough.
    # We include the internal dictionary access for robustness as seen in the notebook.
    current_state = {**tool_context.state._value, **tool_context.state._delta}

    for key, value in current_state.items():
        if key.startswith("user:"):
            clean_key = key.replace("user:", "")
            user_data[clean_key] = value

    return {"status": "success", "data": user_data}