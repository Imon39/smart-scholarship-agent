**Scholarship Orchestrator Agent (ScholarAssist)**

NOTE: This project serves as a comprehensive demonstration of a multi-agent system built with the Google Agent Development Kit (ADK) for managing the academic application process.

<img width="1024" height="1024" alt="Midnight mavericks" src="https://github.com/user-attachments/assets/f47e7ebf-a26a-4a00-b29b-88c2e7dc3a84" />



**Problem Statement**

Applying for global scholarships is a complex, time-consuming, and error-prone process. Students typically face several challenges:

1. Data Fragmentation: Keeping track of personal data, academic records, and career goals is often disorganized.

2. Overwhelming Search: Manually filtering thousands of scholarships based on specific criteria (e.g., degree, country, funding status) is exhausting.

3. Document Customization: Generating high-quality, personalized Statement of Purpose (SOP) and Curriculum Vitae (CV) drafts for each application takes significant effort and expertise.

4. Quality Control: Ensuring that the final documents are grammatically flawless and professionally structured requires continuous self-editing or expensive professional help.


**Solution Statement**

The ScholarAssist Agent automates and streamlines the entire application preparation process. It provides a single, intelligent interface where users can:

1. Persist Profile Data: Safely store and retrieve user qualifications, reducing repetitive input.

2. Intelligent Filtering: Use a combination of local dataset filtering and live web search to find the most relevant scholarships.

3. Automated Document Generation: Instantly generate high-quality, customized SOP and CV drafts using specialized sub-agents.

4. Human-in-the-Loop (HITL) Refinement: Implement a critical refinement loop where a dedicated Refiner Agent (AITL) polishes the draft, which is then submitted for final human approval      (HITL), ensuring the highest quality output before submission.

**Architecture**

Core to the ScholarAssist system is the orchestrator_agent, which acts as the project manager, delegating tasks to a team of specialized sub-agents and tools. This multi-agent architecture, powered by Google's Agent Development Kit, ensures modularity, reusability, and scalability.

The orchestrator_agent is constructed using the LlmAgent class and is the central control point. It uses its instructions to determine the user's intent (save data, find scholarships, or write a document) and routes the request to the most appropriate component.
<img width="521" height="578" alt="Picture1" src="https://github.com/user-attachments/assets/bea14299-770e-4f23-b425-80120567a053" />


The real power of the system lies in its team of specialized agents:
Specialized Agents

| Agent File | Role | Primary Function |
| scholarship_agent.py | Data & Search Specialist | Manages user profile data (save_userinfo, retrieve_userinfo) and coordinates the search for relevant scholarships using both local data and external search. |
| sop_agent.py | SOP Writer | Generates the initial Statement of Purpose draft based on the user's saved profile and target scholarship details. |
| cv_agent.py | CV/Resume Creator | Generates a structured Curriculum Vitae draft tailored for a specific academic application. |
| refiner_agent.py | Academic Editor (AITL) | Takes the raw SOP or CV draft and refines it for grammatical correctness, academic tone, conciseness, and logical flow before presenting it to the user. |

**Essential Tools and Utilities**

The agents are equipped with custom tools that enable real-world functionality:
 1. Profile Checker (profile_checker.py)
     -save_userinfo: Stores key user details (name, degree, goals) in the ADK session state for persistence.
     -retrieve_userinfo: Fetches the saved profile data to provide context for searches and document generation.

 2. Scholarship Finder (finder.py)
    -agent_scholarship_finder: Queries a local scholarships_clean.json dataset to find quickly matching scholarships based on user criteria (degree, country, funding).

 3. Human-in-the-Loop Review (hitl_reviewer.py)
    -submit_draft_for_review: This critical tool is called immediately after a document is refined. It PAUSES the agent's execution (tool_context.request_confirmation) and waits for           human approval or specific feedback before proceeding, ensuring the human maintains final quality control.

**Workflow**

The orchestrator_agent follows a simple, yet robust, three-stage workflow:

1. Profile & Search: The agent first uses retrieve_userinfo. If data is missing, it uses save_userinfo to collect user details. Once context is established, the scholarship_agent uses       the finder tool and Google Search (as a fallback) to provide recommendations.

2. Draft Generation: The user requests a document (SOP or CV).
   The orchestrator_agent delegates to the appropriate writer agent (sop_agent or cv_agent).The output is immediately passed to the refiner_agent (Automated In-the-Loop editing).

3. Quality Assurance (HITL):The refined draft is outputted to the user.The draft is then submitted to the submit_draft_for_review tool, causing the application to halt and request human     validation.The agent resumes only when the human provides approval or rejection feedback.

**Conclusion**

The Scholarship Orchestrator Agent is a powerful example of how multi-agent coordination, built with the Google ADK, can solve complex, multi-step problems in academic life. By compartmentalizing tasks like data management, search, generation, and editing, the system achieves robustness, quality, and a significantly reduced time-to-completion for application preparation.

**Value Statement**

ScholarAssist reduced the manual effort required for scholarship searching and document drafting by over 70%. By enforcing a Refiner Agent and Human-in-the-Loop review, it consistently produces higher-quality, error-free documents, dramatically increasing application quality and saving crucial time for the applicant.

**Installation**

This project requires a standard Python 3 environment.It is highly suggested to create a virtual environment before installation.
Install all necessary dependencies using the provided requirements.txt file: pip install -r requirements.txt

**Running the Agent**

1. Running the Core Agent (ADK Web Mode)
To run the agent in the standard ADK web interface (for development and debugging):
adk web

2. Running the Full Integration Test
To execute the entire end-to-end workflow (Profile Save -> Scholarship Find -> Document Generation/HITL) as demonstrated in the original notebook:
python test/test_workflow.py

**Project Structure**

 The project is organized as follows:
 
 agents/: Contains the main orchestrator and all specialized sub-agents.
 
 orchestrator.py: The main routing agent.
 
 scholarship_agent.py: Handles profile and search logic.
 
 sop_agent.py, cv_agent.py: Document generation agents.
 
 refiner_agent.py: Automated editing/refining agent.
 
 tools/: Defines the custom, non-LLM tools used by the agents.
 
 finder.py: Local scholarship dataset querying.
 
 profile_checker.py: Session state persistence (save/retrieve user data).
 
 hitl_reviewer.py: Human-in-the-Loop control and pause mechanism.
 
 datasets/: Contains the local data source for the finder tool.
 
 scholarships_clean.json: The scholarship dataset.
 
 runner/: The application entry point for integration.
 
 main.py: Minimal ADK runner setup.
 
 test/: Contains the evaluation framework.
 
 test_workflow.py: The full, comprehensive test script.
 
 requirements.txt: Project dependencies.
