from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import BaseChatAgent # type: ignore
from autogen_agentchat.base import Response # type: ignore
from autogen_agentchat.messages import AgentMessage, ChatMessage, TextMessage # type: ignore
from autogen_core.base import CancellationToken # type: ignore
from VertexAI.VertexAI_generator import generate

import asyncio

class VertexAIAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "A VertexAI agent to communicate with Gemini Pro.")

    @property
    def produced_message_types(self) -> List[type[ChatMessage]]:
        return [TextMessage]

    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        user_input = await asyncio.get_event_loop().run_in_executor(None, input, "Enter your response: ")
        gemini_response = generate(user_input)
        return Response(chat_message=TextMessage(content=gemini_response, source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_vertexai_agent() -> None:
    # Create a vertexai agent.
    vertexai_agent = VertexAIAgent("vertexai_agent")
    response = await vertexai_agent.on_messages([], CancellationToken())
    print(response.chat_message.content)

    


# Use asyncio.run(run_vertexai_agent()) when running in a script.
# await run_vertexai_agent()

#asyncio.run(run_vertexai_agent())