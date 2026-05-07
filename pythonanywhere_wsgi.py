import os
import sys

# Path to the current project directory
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

# Import the app and rename it to 'application' for PythonAnywhere
from flask_app import app as application
