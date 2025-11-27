**Scholarship Orchestrator Agent (ScholarAssist) - Integration Tests**

This directory (test/) contains the single, comprehensive integration test (test_workflow.py) designed to validate the entire end-to-end functionality of the ScholarAssist multi-agent system.

**How to Run the Test**

The test is implemented as a standalone asynchronous Python script. You can run the test from the root directory of the project using the following command:

python test/test_workflow.py


**⚠️ Prerequisite**

The test script automatically creates and cleans up a local database file named test_workflow_data.db to ensure a clean slate for every run.

**Test Scenario: Full Workflow Simulation**

The test_workflow.py script runs the orchestrator_agent through a predefined, three-step sequence of user queries. This integration test ensures that all agents and tools are correctly coordinating in a multi-turn, stateful conversation.

  **Step**                 

1: Save Profile

    Saving academic background (MBA, PhD Management).

    orchestrator_agent, save_userinfo (Tool)

    Confirms the system can successfully save and persist user data across turns.

2: Find Scholarships

    Searching for PhD Management scholarships in the USA/UK.

    scholarship_agent, retrieve_userinfo, agent_scholarship_finder (Tool), Google Search (Fallback)

    Confirms the agent can retrieve profile context and execute the search logic.

3: Document Generation & Review

    Requesting an SOP for Oxford University, focusing on research.

    orchestrator_agent, sop_agent, refiner_agent, submit_draft_for_review (HITL Tool)

Crucial Step: Validates the entire complex pipeline (Generate -> Refine/AITL -> Pause for Human Review/HITL).
The script will print the agent's full streamed response for each query to the console, allowing for easy observation and validation of the workflow.

The script will print the agent's full streamed response for each query to the console, allowing for easy observation and validation of the workflow.
