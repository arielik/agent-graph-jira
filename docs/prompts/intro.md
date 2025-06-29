act as a senior python developer, ai engineer with vast experience in development.
You're starting a new project which will leverage ai, in particular it will be an agentic solution that will connet with different llm, use a vector db for rag, use prompts to specifically ask refined questions, and will use langgraph. create a folder structure with best practices, in particular i like to have the following folder structure as miniimum/startng point (viewed from parent folder):

- data/
- notebooks/
- src/
  - core/
    - agent/
    - prompts/
    - tools/
  - utils/
  - infrastructure/
    - vector_database/
    - llm_clients/
- tools/
- tests/
- Makefile
- README
- pyproject.toml
- .env
- .python-version

your task is to create this layout and create a readme file that explains how this repo will be used.


---

I want to create a system that reads from a input yaml file and generates jira stories below a jira cloud instance. Details such as project, label and other general attributes will come from global entry in the yaml as well.

The YAML will look like the example-stories.yaml attached.

I'm planning to use integration with langgraph, so it will read each yaml entry, it will ask the llm to "expand it" then it will go to a jira node that will take care of actually hitting the api of jira for the creation (using the details as projects, labels, components, etc from the yaml). The "expand" is going to take place leveraging a specialized prompt that i want to store under a prompts folder
