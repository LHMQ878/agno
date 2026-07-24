"""
AgentQL Tools for scraping websites.

Prerequisites:
1. pip install agentql
2. playwright install
3. export AGENTQL_API_KEY=your_key  # from https://agentql.com/
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.agentql import AgentQLTools

# Basic scraping
agent = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[AgentQLTools()],
)

# Custom query
custom_query = "{ title text_content[] }"
custom_agent = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[AgentQLTools(agentql_query=custom_query, custom_scrape_website=True)],
)

if __name__ == "__main__":
    agent.print_response("Scrape https://docs.agno.com/introduction", markdown=True)
