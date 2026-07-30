"""Regression tests for https://github.com/agno-agi/agno/issues/9251.

``StopAgentRun(agent_message=...)`` ends the run, so no model turn follows to speak for it.
The message was only appended to history, leaving the run's content empty and the caller with
no visible reason for the stop.

A tool that stops the run declaratively (``@tool(stop_after_tool_call=True)``) already surfaces
its output, because the decorator turns on ``show_result``. These tests pin that both stop paths
behave the same, and that the paths which are *not* supposed to surface a message still don't.
"""

from dataclasses import dataclass
from typing import Any, AsyncIterator, Iterator, List

import pytest

from agno.agent import Agent
from agno.exceptions import RetryAgentRun, StopAgentRun
from agno.models.base import Model
from agno.models.message import Message
from agno.models.response import ModelResponse
from agno.run.agent import RunEvent
from agno.tools import tool

SECOND_TURN = "MODEL-SECOND-TURN"


@dataclass
class StubModel(Model):
    """Requests one tool call on the first turn, then answers with plain text.

    The second turn only happens if the run was *not* stopped, so ``turns`` doubles as a probe
    for whether the stop actually took effect.
    """

    id: str = "stub"
    name: str = "Stub"
    provider: str = "Stub"
    tool_to_call: str = "stop_tool"
    turns: int = 0

    def get_provider(self) -> str:
        return "Stub"

    def _next_response(self) -> ModelResponse:
        self.turns += 1
        if self.turns == 1:
            return ModelResponse(
                role="assistant",
                content=None,
                tool_calls=[
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {"name": self.tool_to_call, "arguments": "{}"},
                    }
                ],
            )
        return ModelResponse(role="assistant", content=SECOND_TURN)

    def invoke(self, *args, **kwargs) -> ModelResponse:
        return self._next_response()

    async def ainvoke(self, *args, **kwargs) -> ModelResponse:
        return self._next_response()

    def invoke_stream(self, *args, **kwargs) -> Iterator[ModelResponse]:
        yield self._next_response()

    async def ainvoke_stream(self, *args, **kwargs) -> AsyncIterator[ModelResponse]:
        yield self._next_response()

    def _parse_provider_response(self, response: Any, **kwargs) -> ModelResponse:
        return response

    def _parse_provider_response_delta(self, response: Any) -> ModelResponse:
        return response


def _agent(func: Any, tool_name: str) -> Agent:
    return Agent(model=StubModel(tool_to_call=tool_name), tools=[func], telemetry=False)


def _streamed_content(agent: Agent) -> List[Any]:
    return [
        event.content
        for event in agent.run("go", stream=True, stream_events=True)
        if getattr(event, "event", None) == RunEvent.run_content.value and event.content
    ]


async def _astreamed_content(agent: Agent) -> List[Any]:
    contents = []
    async for event in agent.arun("go", stream=True, stream_events=True):
        if getattr(event, "event", None) == RunEvent.run_content.value and event.content:
            contents.append(event.content)
    return contents


STOP_MESSAGE = "Value 200 exceeds threshold. Stopping tool call execution."


def stop_with_message() -> str:
    """Stop the run and explain why."""
    raise StopAgentRun(exc="Value 200 exceeds threshold.", agent_message=STOP_MESSAGE)


def test_stop_agent_run_agent_message_is_run_content() -> None:
    agent = _agent(stop_with_message, "stop_with_message")

    run_output = agent.run("go")

    assert run_output.content == STOP_MESSAGE
    # The run really stopped: the model was never asked for a second turn.
    assert agent.model.turns == 1  # type: ignore[union-attr]
    # And the message is still in history, as it was before.
    assert any(m.role == "assistant" and m.content == STOP_MESSAGE for m in run_output.messages or [])


def test_stop_agent_run_agent_message_is_streamed() -> None:
    agent = _agent(stop_with_message, "stop_with_message")

    assert _streamed_content(agent) == [STOP_MESSAGE]


@pytest.mark.asyncio
async def test_stop_agent_run_agent_message_is_run_content_async() -> None:
    agent = _agent(stop_with_message, "stop_with_message")

    run_output = await agent.arun("go")

    assert run_output.content == STOP_MESSAGE
    assert agent.model.turns == 1  # type: ignore[union-attr]


@pytest.mark.asyncio
async def test_stop_agent_run_agent_message_is_streamed_async() -> None:
    agent = _agent(stop_with_message, "stop_with_message")

    assert await _astreamed_content(agent) == [STOP_MESSAGE]


def stop_with_message_object() -> str:
    """Stop the run with a Message rather than a plain string."""
    raise StopAgentRun(exc="stopping", agent_message=Message(role="assistant", content=STOP_MESSAGE))


def test_stop_agent_run_accepts_a_message_object() -> None:
    """``agent_message`` is typed ``Union[str, Message]``, so both forms must surface."""
    agent = _agent(stop_with_message_object, "stop_with_message_object")

    assert agent.run("go").content == STOP_MESSAGE


@tool(stop_after_tool_call=True)
def stop_declaratively() -> str:
    """Stop the run by returning."""
    return "DECLARATIVE-RESULT"


def test_declarative_stop_still_shows_its_result() -> None:
    """The precedent this fix aligns with — unchanged."""
    agent = _agent(stop_declaratively, "stop_declaratively")

    assert agent.run("go").content == "DECLARATIVE-RESULT"


def stop_without_message() -> str:
    """Stop the run without explaining why."""
    raise StopAgentRun(exc="stopping")


def test_stop_agent_run_without_agent_message_adds_no_content() -> None:
    """Nothing to show, so nothing is invented."""
    agent = _agent(stop_without_message, "stop_without_message")

    run_output = agent.run("go")

    assert not run_output.content
    assert agent.model.turns == 1  # type: ignore[union-attr]


def stop_with_user_message_only() -> str:
    """Stop the run, addressing the model rather than the caller."""
    raise StopAgentRun(exc="stopping", user_message="USER-MESSAGE")


def test_stop_agent_run_user_message_is_not_run_content() -> None:
    """``user_message`` is input for the model, not output for the caller."""
    agent = _agent(stop_with_user_message_only, "stop_with_user_message_only")

    assert not agent.run("go").content


def retry_with_message() -> str:
    """Ask the model to try again, with guidance."""
    raise RetryAgentRun(exc="retry", agent_message="RETRY-GUIDANCE")


def test_retry_agent_run_agent_message_stays_internal() -> None:
    """A retried run continues, so the model speaks for itself and the guidance stays hidden."""
    agent = _agent(retry_with_message, "retry_with_message")

    run_output = agent.run("go")

    assert run_output.content == SECOND_TURN
    assert "RETRY-GUIDANCE" not in str(run_output.content)
    assert agent.model.turns == 2  # type: ignore[union-attr]


@pytest.mark.asyncio
async def test_retry_agent_run_agent_message_stays_internal_async() -> None:
    agent = _agent(retry_with_message, "retry_with_message")

    run_output = await agent.arun("go")

    assert run_output.content == SECOND_TURN
    assert agent.model.turns == 2  # type: ignore[union-attr]
