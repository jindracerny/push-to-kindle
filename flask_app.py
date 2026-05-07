import os
from pathlib import Path
from dotenv import load_dotenv # Remember this import
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 1. Load .env (KEY STEP)
base_path = Path(__file__).parent
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
CORS(app)

# 2. Načtení konfigurace
KINDLE_EMAIL = os.getenv('KINDLE_EMAIL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = 465 # For Gmail on PythonAnywhere (if you have a paid account) 465/SSL is more stable

@app.route('/send', methods=['POST'])
def send_to_kindle():
    data = request.json
    title = data.get('title', 'Webpage Content')
    body = data.get('body', '')

    if not body:
        return jsonify({"error": "No content to send"}), 400

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = KINDLE_EMAIL
        msg['Subject'] = title  # Sets the email subject

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            <div style="white-space: pre-wrap;">{body}</div>
        </body>
        </html>
        """

        # Dynamic filename without unsafe characters
        clean_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).strip()
        filename = f"{clean_title or 'article'}.html"

        attachment = MIMEApplication(html_content.encode('utf-8'))
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return jsonify({"status": "success", "sent_title": title}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500