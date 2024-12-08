# My Python Application

This is a versatile Python application that can be run in two modes:
1. **Menu-driven Mode**: A terminal-based interactive menu.
2. **Flask App**: A web application powered by Flask.

## Getting Started

Follow the steps below to set up and run the application:

```bash
# Clone the Repository
git clone <repository_url>
cd <repository_name>

# Create a Virtual Environment
python -m venv venv

# Activate the Virtual Environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Create a .env File
# In the root directory, create a file named `.env` and add the following:
VERTEXAI_API_KEY=YOUR_API_KEY
# Replace `YOUR_API_KEY` with your actual API key

# Running the Application

## Menu-driven Mode:
python menu_driven_main.py

## Flask Web App:
python web_app_main.py
# Access the Flask app at: http://127.0.0.1:5000
