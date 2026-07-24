"""Run `uv pip install openai` to install dependencies."""

from pathlib import Path

from agno.agent import Agent
from agno.tools.openai import OpenAITools
from agno.utils.media import download_image

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------


# Example 1: Basic image generation agent with all OpenAI tools enabled
agent = Agent(tools=[OpenAITools(all=True)], name="Image Generator")

# Example 2: Enable only image generation
agent_specific = Agent(
    tools=[
        OpenAITools(
            transcription=False,
            speech_generation=False,
            image_model="gpt-image-2",
            image_size="1024x1024",
        )
    ],
    name="Basic Image Generator",
)

# Example 3: High-quality custom image generator
custom_openai = OpenAITools(
    transcription=False,
    speech_generation=False,
    image_model="gpt-image-2",
    image_size="1792x1024",
    image_quality="hd",
)

agent_custom = Agent(
    tools=[custom_openai],
    name="Custom Image Generator",
)

# Test basic generation

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "Generate an image of a futuristic city with flying cars and tall skyscrapers",
        markdown=True,
    )

    response = agent_custom.run(
        "Create a panoramic nature scene showing a peaceful mountain lake at sunset",
        markdown=True,
    )
    if response.images and response.images[0].url:
        download_image(
            url=response.images[0].url,
            output_path=str(Path(__file__).parent.joinpath("tmp/nature.jpg")),
        )
