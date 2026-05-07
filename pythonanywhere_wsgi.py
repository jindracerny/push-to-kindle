import os
import sys

# Path to your files
path = '/home/jindracerny/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

# Import the app and rename it to 'application' for PythonAnywhere
from flask_app import app as application
