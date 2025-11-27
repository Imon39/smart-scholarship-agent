# tools/hitl_reviewer.py

from google.adk.tools import ToolContext


def submit_draft_for_review(
        draft_text: str, document_type: str, tool_context: ToolContext
) -> dict:
    """
    Submits a draft (SOP or CV) for human review.
    This tool PAUSES execution until the human approves or rejects (Human-in-the-Loop).
    """

    # SCENARIO 1: First call - PAUSE for Human Review
    if not tool_context.tool_confirmation:
        # Request confirmation (PAUSE)
        tool_context.request_confirmation(
            hint=f"Review {document_type} Draft",
            payload={
                "document_type": document_type,
                "draft_text": draft_text
            },
        )

        return {
            "status": "pending_review",
            "message": f"Draft submitted. Waiting for human feedback on: {document_type}"
        }

    # SCENARIO 2: Resuming after Human Decision
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "message": "The human APPROVED the draft. You can now finalize formatting and output the result."
        }
    else:
        return {
            "status": "rejected",
            "message": "The human REJECTED the draft. Please ask the user for specific feedback on what to change."
        }