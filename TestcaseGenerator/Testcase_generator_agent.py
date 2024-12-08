from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import BaseChatAgent # type: ignore
from autogen_agentchat.base import Response # type: ignore
from autogen_agentchat.messages import AgentMessage, ChatMessage, TextMessage # type: ignore
from autogen_core.base import CancellationToken # type: ignore
from VertexAI.VertexAI_generator import generate

import asyncio
import json

class TestcaseGeneratorAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "A Testcase Generator agent to generate testcases.")

    @property
    def produced_message_types(self) -> List[type[ChatMessage]]:
        return [TextMessage]
    
    def convert_testcases_to_list(self, testcases: str) -> List:
        print(testcases)
        list_object = json.loads(testcases)
        with open('Artifacts/test_cases.json', 'w') as f:
            json.dump(list_object, f, indent=4)
        return list_object
    
    def generate_testcases(self, no_of_cases, scenario, requirement):
        sample_json = str({
            "endpoint": "/endpoint",
            "method": "GET/POST/etc",
            "body": "JSON body",
            "expectedOutput": "JOSN body"
        })
        final_query = f"""You are a software QA expert, I want you to write a set of {no_of_cases} test cases to test the following scenario: {scenario}. You need to write the test cases in such a way that, all the corner cases are covered, and the given requirement is met. The given requirement is : {requirement}. I want you to respond only with a list of JSON objects.
        
        For example:
        You have to test an API with n routes, and you need to generate 3 cases for each route, then you have to respond with
        3*n JSON objects in the list. In which each JSON object needs to have an appropriate structure. Say, for this API, it can be as follows:
        {sample_json}
        
        Respond with the respective number of JSON objects, total number of JSON objects = {no_of_cases} in the list only(so that it can be parsed with json.load in python), make sure endpoints are complete with full hostname as mentioned in the scenario/requirements. STRICTLY DO NOT RESPOND WITH ANYTHING ELSE!
        """
        testcases = generate(final_query)
        return Response(chat_message=TextMessage(content=testcases, source=self.name))

    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        no_of_cases = await asyncio.get_event_loop().run_in_executor(None, input, "Enter number of testcases: ")
        scenario = await asyncio.get_event_loop().run_in_executor(None, input, "Enter detailed scenario: ")
        requirement = await asyncio.get_event_loop().run_in_executor(None, input, "Enter requirement: ")
        sample_json = str({
            "endpoint": "/full-endpoint-with-hostname",
            "method": "GET/POST/etc",
            "body": "JSON body",
            "expectedOutput": "JOSN body"
        })
        final_query = f"""You are a software QA expert, I want you to write a set of {no_of_cases} test cases to test the following scenario: {scenario}. You need to write the test cases in such a way that, all the corner cases are covered, and the given requirement is met. The given requirement is : {requirement}. I want you to respond only with a list of JSON objects.
        
        For example:
        You have to test an API with n routes, and you need to generate 3 cases for each route, then you have to respond with
        3*n JSON objects in the list. In which each JSON object needs to have an appropriate structure. Say, for this API, it can be as follows:
        {sample_json}
        
        Respond with the respective number of JSON objects, total number of JSON objects = {no_of_cases} in the list only(so that it can be parsed with json.load in python), make sure endpoints are complete with full hostname as mentioned in the scenario/requirements. STRICTLY DO NOT RESPOND WITH ANYTHING ELSE!
        """
        testcases = generate(final_query)
        return Response(chat_message=TextMessage(content=testcases, source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_testcase_generator_agent() -> None:
    # Create a vertexai agent.
    testcase_generator_agent = TestcaseGeneratorAgent("testcase_generator_agent")
    response = await testcase_generator_agent.on_messages([], CancellationToken())
    testcases = response.chat_message.content
    return testcase_generator_agent.convert_testcases_to_list(testcases)

    


# Use asyncio.run(run_vertexai_agent()) when running in a script.
# await run_vertexai_agent()

#asyncio.run(run_vertexai_agent())