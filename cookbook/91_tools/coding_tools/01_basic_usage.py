"""
CodingTools: Read-Only by Default
==================================
CodingTools provides safe read-only exploration out of the box. Write and
shell capabilities are opt-in for security.

Read-only tools (enabled by default):
- read_file: Read files with line numbers and pagination
- run_grep: Search file contents
- run_find: Search for files by glob pattern
- run_ls: List directory contents

Write tools (opt-in):
- edit_file: Exact text find-and-replace with diff output
- write_file: Create or overwrite files
- run_shell: Execute shell commands with timeout

Enable write tools with: CodingTools(edit_file=True, write_file=True, run_shell=True)
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.coding import CodingTools

# ---------------------------------------------------------------------------
# Create Agent with CodingTools
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[CodingTools(base_dir=".")],
    instructions="You are a coding assistant. Use the coding tools to help the user.",
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "List the files in the current directory and read the README.md file if it exists.",
        stream=True,
    )
