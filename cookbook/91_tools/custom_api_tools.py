"""CustomApiTools - make HTTP requests to any API."""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.api import CustomApiTools

agent = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[CustomApiTools(base_url="https://dog.ceo/api")],
)

if __name__ == "__main__":
    agent.print_response("GET /breeds/image/random and /breeds/list/all")
