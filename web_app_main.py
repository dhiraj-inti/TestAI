from flask import Flask, render_template, request, jsonify, send_file
from TestcaseGenerator.Testcase_generator_agent import TestcaseGeneratorAgent
from TestcaseExecutor.Testcase_executor_agent import run_testcase_executor_agent
from TestcaseReportGenerator.Testcase_report_generator_agent import run_testcase_report_generator_agent

import asyncio

app = Flask(__name__)

def check_data(a,b):
    if not isinstance(a,int) or not isinstance(b, int):
        return True

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    a = data.get('a')
    b = data.get('b')

    if a is None or b is None:
        return jsonify({'error': 'Missing parameters'}), 400
    
    if check_data(a,b):
        return jsonify({'error': 'Invalid parameters'}), 400

    result = a + b
    return jsonify({'result': result})

@app.route('/sub', methods=['POST'])
def subtract():
    data = request.get_json()
    a = data.get('a')
    b = data.get('b')

    if a is None or b is None:
        return jsonify({'error': 'Missing parameters'}), 400
    
    if check_data(a,b):
        return jsonify({'error': 'Invalid parameters'}), 400

    result = a - b
    return jsonify({'result': result})

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.get_json()
    a = data.get('a')
    b = data.get('b')


    if a is None or b is None:
        return jsonify({'error': 'Missing parameters'}), 400
    
    if check_data(a,b):
        return jsonify({'error': 'Invalid parameters'}), 400

    result = a * b
    return jsonify({'result': result})

@app.route('/divide', methods=['POST'])
def divide():
    data = request.get_json()
    a = data.get('a')
    b = data.get('b')

    if a is None or b is None:
        return jsonify({'error': 'Missing parameters'}), 400

    if b == 0:
        return jsonify({'error': 'Division by 0 is not allowed'}), 400
    
    if check_data(a,b):
        return jsonify({'error': 'Invalid parameters'}), 400

    result = a / b
    return jsonify({'result': result})

@app.route('/testcaseGenerator', methods=['POST'])
def testcaseGenerator():
    data = request.get_json()  # Parses the JSON body
    number_of_testcases = data.get('number_of_testcases')
    scenario = data.get('scenario')
    requirement = data.get('requirement')

    testcase_generator_agent = TestcaseGeneratorAgent("testcase_generator_agent")
    response = testcase_generator_agent.generate_testcases(number_of_testcases, scenario, requirement)
    testcases = testcase_generator_agent.convert_testcases_to_list(response.chat_message.content)
    return {"testcases":testcases, "success":True},200

@app.route('/testcaseExecutor', methods=['POST'])
def testcaseExecutor():
    asyncio.run(run_testcase_executor_agent())
    return {"success":True},200

@app.route('/testcaseReport', methods=['POST'])
def testcaseReport():
    asyncio.run(run_testcase_report_generator_agent())
    return {"success":True},200


@app.route('/testcaseReport/download', methods=['GET'])
def download_report():
    return send_file(
        "Artifacts/test_cases_report.pdf",
        as_attachment=True,
        download_name="test_cases_report.pdf",
        mimetype="application/pdf"
    )


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=True)