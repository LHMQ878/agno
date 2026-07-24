"""
ArxivTools - search and read academic papers.

pip install arxiv pypdf
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.arxiv import ArxivTools

# Default: both search and read enabled
agent = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[ArxivTools()],
)

# Search only (no PDF reading)
agent_search_only = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[ArxivTools(search_arxiv=True, read_arxiv_papers=False)],
)

# All tools explicitly
agent_all = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[ArxivTools(all=True)],
)

if __name__ == "__main__":
    agent.print_response("Search arxiv for 'language models' and summarize top 3")
