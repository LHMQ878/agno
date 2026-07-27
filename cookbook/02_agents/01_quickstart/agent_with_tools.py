"""
Agent With Tools
=============================

Agent With Tools Quickstart.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Tool-Enabled Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[WebSearchTools(backend="duckduckgo")],
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "Find one recent AI safety headline and summarize it.", stream=True
    )
