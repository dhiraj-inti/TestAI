from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import BaseChatAgent # type: ignore
from autogen_agentchat.base import Response # type: ignore
from autogen_agentchat.messages import AgentMessage, ChatMessage, TextMessage # type: ignore
from autogen_core.base import CancellationToken # type: ignore

import json
import pandas as pd
from fpdf import FPDF # type: ignore

class TestcaseReportGeneratorAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "A Testcase Report Generator agent to execute testcases.")
        self.testcases_executed = []

    @property
    def produced_message_types(self) -> List[type[ChatMessage]]:
        return [TextMessage]
    
    def read_testcases_executed(self):
        with open('Artifacts/test_cases_executed.json', 'r') as f:
            self.testcases_executed = json.load(f)

    def generate_pdf_report(self):
        data = self.testcases_executed
    
        # Convert JSON data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Handle potential KeyError for 'FAIL' status
        try:
            failed_count = df['status'].value_counts()['FAIL']
        except KeyError:
            failed_count = 0

        # Create a PDF object
        pdf = FPDF(orientation='L', unit='mm', format='A4')  # Landscape mode
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        # Add a title
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, txt="API Test Report", ln=1, align='C')
        pdf.ln(5)

        # Add table header
        pdf.set_font("Arial", style="B", size=10)
        pdf.set_fill_color(200, 200, 200)
        headers = ["Testcase #", "Endpoint", "Method", "Body", "Expected Output", "Received Output", "Status"]
        column_widths = [20, 60, 20, 50, 50, 50, 20]  # Adjust column widths for better layout

        for header, width in zip(headers, column_widths):
            pdf.cell(width, 10, txt=header, border=1, fill=True, align='C')
        pdf.ln()

        # Add table rows with text wrapping
        pdf.set_font("Arial", size=10)
        for index, row in df.iterrows():
            pdf.cell(column_widths[0], 10, txt=str(index), border=1, align='L')
            pdf.multi_cell(column_widths[1], 10, txt=row['endpoint'], border=1, align='L', ln=3, max_line_height=pdf.font_size)  # Wrap Endpoint
            pdf.cell(column_widths[2], 10, txt=row['method'], border=1, align='L')
            pdf.multi_cell(column_widths[3], 10, txt=json.dumps(row['body']), border=1, align='L', ln=3, max_line_height=pdf.font_size)  # Wrap Body
            pdf.multi_cell(column_widths[4], 10, txt=json.dumps(row['expectedOutput']), border=1, align='L', ln=3, max_line_height=pdf.font_size)  # Wrap Expected Output
            pdf.multi_cell(column_widths[5], 10, txt=row['receivedOutput'], border=1, align='L', ln=3, max_line_height=pdf.font_size)  # Wrap Received Output

            # Highlight status with colors
            if row['status'] == "PASS":
                pdf.set_text_color(0, 128, 0)  # Green for PASS
            else:
                pdf.set_text_color(255, 0, 0)  # Red for FAIL
            pdf.cell(column_widths[6], 10, txt=row['status'], border=1, align='C', ln=1)
            pdf.set_text_color(0, 0, 0)  # Reset color for next row

        # Add a summary section
        pdf.ln(10)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, txt="Summary:", ln=1)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, txt=f"Total Test Cases: {len(df)}", ln=1)
        pdf.cell(0, 10, txt=f"Passed: {df['status'].value_counts().get('PASS', 0)}", ln=1)
        pdf.cell(0, 10, txt=f"Failed: {failed_count}", ln=1)

        # Save the PDF
        pdf.output("Artifacts/test_cases_report.pdf")
        print("Report generated: Artifacts/test_cases_report.pdf")
            

    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        pass

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_testcase_report_generator_agent() -> None:
  
    testcase_executor_agent = TestcaseReportGeneratorAgent("testcase_report_generator_agent")
    testcase_executor_agent.read_testcases_executed()
    testcase_executor_agent.generate_pdf_report()
