# tools/finder.py

import json
import os
from google.adk.tools import AgentTool  # though its not used here but needed
# these path can be chnage depend on dataset location
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datasets",
                            "scholarships_clean.json")


def find_scholarships(profile: dict, dataset_path: str, top_k: int = 5):
    """Core logic to filter scholarships based on degree, country, and funding preference."""
    try:
        # Load dataset from the specified path (which can be local or an absolute path)
        with open(dataset_path, "r") as f:
            scholarships = json.load(f)
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to load dataset: {str(e)}"}

    eligible = []

    # Clean up funding preference for comparison
    funding_pref = str(profile.get("funding", "")).lower().replace("$", "").replace(",", "")

    for s in scholarships:
        # Degree check
        degree_ok = (
                str(profile.get("degree", "")).lower() == "any"
                or profile.get("degree") in s.get("degrees", "")
        )

        # Country check
        country_ok = (
                str(profile.get("country", "")).lower() == "any"
                or profile.get("country", "").lower() in s.get("location", "").lower()
        )

        if degree_ok and country_ok:
            score = 0

            scholarship_funds_str = str(s.get("funds", "")).lower().replace("$", "").replace(",", "")

            # Simple scoring based on funding match
            if funding_pref == "any" or funding_pref in scholarship_funds_str:
                score += 1

            s["score"] = score
            eligible.append(s)

    if not eligible:
        return {"status": "success", "scholarships": [], "message": "No matching scholarships found"}

    return {
        "status": "success",
        "scholarships": sorted(eligible, key=lambda x: x["score"], reverse=True)[:top_k]
    }


def agent_scholarship_finder(profile: dict, top_k: int = 5) -> dict:
    """Wrapper function to find scholarships using the local dataset path."""
    # Note: If running locally outside Kaggle, DATASET_PATH needs to be correct.
    return find_scholarships(profile=profile, dataset_path=DATASET_PATH, top_k=top_k)