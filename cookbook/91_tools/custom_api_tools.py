"""
CustomApiTools - make HTTP requests to any API.

Args:
    base_url: Base URL for API calls
    username: Username for basic authentication
    password: Password for basic authentication
    api_key: API key for authentication
    headers: Default headers to include in requests
    verify_ssl: Whether to verify SSL certificates
    timeout: Request timeout in seconds
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.api import CustomApiTools

# Example 1: Basic usage
agent = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[CustomApiTools(base_url="https://dog.ceo/api")],
)

# Example 2: Enable all functions
agent_all = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[CustomApiTools(base_url="https://dog.ceo/api", all=True)],
)

if __name__ == "__main__":
    agent.print_response(
        'Make api calls to /breeds/image/random and /breeds/list/all to get a random dog image and list of dog breeds. Use method="GET" for both.'
    )
