"""
AgentQL Tools for scraping websites.

Prerequisites:
1. pip install agentql
2. playwright install
3. export AGENTQL_API_KEY=your_key  # from https://agentql.com/

AgentQL will open up a browser instance (don't close it) and do scraping on the site.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.agentql import AgentQLTools

# Example 1: Basic scraping (default)
agent = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[AgentQLTools()],
)

# Example 2: Enable all functions
agent_all = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[AgentQLTools(all=True, agentql_query="your_query_here")],
)

# Example 3: Custom query with specific function enabled
custom_query = """
{
    title
    text_content[]
}
"""

custom_agent = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[
        AgentQLTools(
            scrape_website=True,
            custom_scrape_website=True,
            agentql_query=custom_query,
        )
    ],
)

if __name__ == "__main__":
    agent.print_response(
        "Scrape the main content from https://docs.agno.com/introduction", markdown=True
    )
    custom_agent.print_response(
        "Extract title and content from https://docs.agno.com/introduction",
        markdown=True,
    )
