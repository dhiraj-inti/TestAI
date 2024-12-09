from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import BaseChatAgent # type: ignore
from autogen_agentchat.base import Response # type: ignore
from autogen_agentchat.messages import AgentMessage, ChatMessage, TextMessage # type: ignore
from autogen_core.base import CancellationToken # type: ignore

import asyncio
import json
import requests

class TestcaseExecutorAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "A Testcase Executor agent to execute testcases.")
        self.testcases = []

    @property
    def produced_message_types(self) -> List[type[ChatMessage]]:
        return [TextMessage]
    
    def read_testcases(self):
        with open('Artifacts/test_cases.json', 'r') as f:
            self.testcases = json.load(f)

    async def run_testcases(self):
        testcase_executions = []
        test_cases = self.testcases
        for test_case in test_cases:
            url = test_case['endpoint']
            method = test_case['method']
            body = json.loads(str(test_case['body']))  # Parse the JSON body
            expected_output = test_case['expectedOutput']

            if method == 'POST':
                response = requests.post(url, json=body)
            elif method == 'GET':
                response = requests.get(url)
            # Add more methods as needed (e.g., PUT, DELETE)
            response_json = response.json()
            test_case["receivedOutput"] = json.dumps(response_json)

            if test_case["receivedOutput"] == expected_output:
                test_case["status"] = "PASS"
            else:
                test_case["status"] = "FAIL"

            testcase_executions.append(test_case)

        return testcase_executions
            

    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        pass

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_testcase_executor_agent() -> None:
    # Create a vertexai agent.
    testcase_executor_agent = TestcaseExecutorAgent("testcase_executor_agent")
    testcase_executor_agent.read_testcases()
    testcase_executions = await testcase_executor_agent.run_testcases()
    with open('Artifacts/test_cases_executed.json', 'w') as f:
        json.dump(testcase_executions, f, indent=4)

    print("\n\n====Check test_cases_executed.json====\n\n")

    


# Use asyncio.run(run_vertexai_agent()) when running in a script.
# await run_vertexai_agent()

#asyncio.run(run_vertexai_agent())