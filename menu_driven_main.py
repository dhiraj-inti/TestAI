import asyncio
from VertexAI.VertexAI_agent import run_vertexai_agent
from TestcaseGenerator.Testcase_generator_agent import run_testcase_generator_agent
from TestcaseExecutor.Testcase_executor_agent import run_testcase_executor_agent
from TestcaseReportGenerator.Testcase_report_generator_agent import run_testcase_report_generator_agent


while True:
    choice = int(input("Enter the choice to run the agent:\n\n1. Vertex AI\n2. Testcase Generator\n3. Testcase Executor\n4. Testcase Report Generator\n\nEnter your choice: "))
    match choice:
        case 1:
            asyncio.run(run_vertexai_agent())
        case 2:
            testcases = asyncio.run(run_testcase_generator_agent())
            print(type(testcases))
            print(testcases)
        case 3:
            asyncio.run(run_testcase_executor_agent())
        case 4:
            asyncio.run(run_testcase_report_generator_agent())
        case 0:
            break
            
    
