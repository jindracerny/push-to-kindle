# Send to Kindle

This project allows you to send webpage content to your Kindle device via email.

## Components

1.  **Flask Backend (`flask_app.py`)**: Runs on PythonAnywhere. Receives content and sends it to your Kindle email.
2.  **Chrome Extension**: Works on Desktop and mobile browsers that support extensions (e.g., Kiwi Browser on Android).
3.  **Bookmarklet**: A universal way to send content from mobile browsers (Chrome, Safari).

## Local Development

1.  Install dependencies:
    ```bash
    pip install flask flask-cors python-dotenv
    ```
2.  Your `.env` file is already configured with your credentials.
3.  Run locally:
    ```bash
    python flask_app.py
    ```
4.  Test the endpoint:
    ```bash
    curl -X POST http://localhost:5000/send \
      -H "Content-Type: application/json" \
      -d '{"title":"Test","body":"Hello Kindle"}'
    ```

## Configuration

Before deploying, you **must** substitute the following placeholders with your actual values:

- **`<your-domain>`** in `manifest.json` and `background.js` → Replace with your PythonAnywhere username (e.g., `username` if your domain is `username.pythonanywhere.com`)
- **`<your-pythonanywhere-domain>`** in the bookmarklet → Replace with your full PythonAnywhere domain (e.g., `username.pythonanywhere.com`)

Example: If your PythonAnywhere domain is `myaccount.pythonanywhere.com`, change:
- `https://<your-domain>.pythonanywhere.com/*` → `https://myaccount.pythonanywhere.com/*`
- `https://<your-pythonanywhere-domain>.pythonanywhere.com/send` → `https://myaccount.pythonanywhere.com/send`

Also configure your credentials in the `.env` file (see Setup section below).

## Setup

### 1. Backend (PythonAnywhere)

1.  Upload `flask_app.py`, `.env`, and `pythonanywhere_wsgi.py` to PythonAnywhere.
2.  In the PythonAnywhere Web app settings, set the WSGI configuration file to `pythonanywhere_wsgi.py`.
3.  Install dependencies in your virtual environment:
    ```bash
    pip install flask flask-cors python-dotenv
    ```
4.  Set the following **Environment Variables** in your PythonAnywhere account:

    **Option A: Using .env file (Recommended - upload your existing .env)**
    - Your `.env` file is already configured locally
    - Upload it to your PythonAnywhere directory
    - The Flask app will automatically load it

    **Option B: Using Web App Configuration**
    - Go to [pythonanywhere.com](https://www.pythonanywhere.com)
    - Click on "Web" in the top menu
    - Click on your web app name
    - Scroll down to **"Environment variables"**
    - Add:
      ```
      KINDLE_EMAIL = yourname@kindle.com
      SENDER_EMAIL = yourname@gmail.com
      SENDER_PASSWORD = xxxx xxxx xxxx xxxx (your 16-char App Password)
      ```
    - Click "Save"
    - Reload your web app

    **Option C: Using a separate .env file on PythonAnywhere**
    - Upload a `.env` file to your PythonAnywhere directory with:
      ```
      KINDLE_EMAIL=yourname@kindle.com
      SENDER_EMAIL=yourname@gmail.com
      SENDER_PASSWORD=xxxx xxxx xxxx xxxx
      ```
    
    **To get your Gmail App Password:**
    - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
    - Select "Mail" and "Windows Computer"
    - Copy the 16-character password and use it as `SENDER_PASSWORD`

4.  Whitelist the `SENDER_EMAIL` in your Amazon account:
    - Go to [amazon.com/managecontent](https://www.amazon.com/managecontent)
    - Find "Approved Personal Document E-mail List"
    - Add your `SENDER_EMAIL` address

### 2. Chrome Extension

1.  Open `chrome://extensions`.
2.  Enable "Developer mode".
3.  Click "Load unpacked" and select the `push2Kindle` folder.

### 3. Mobile (Bookmarklet)

Since Chrome for mobile doesn't support extensions, use this bookmarklet:

1.  Create a new bookmark in your mobile browser.
2.  Name it "Send to Kindle".
3.  Paste the following into the URL field (do not forget to edit the url to fetch):

```
javascript:(function(){
    const h1 = document.querySelector('h1');
    const t = h1 ? h1.innerText.trim() : document.title;
    
    let root = document.querySelector('article') || document.querySelector('main') || document.body;
    
    /* Aggressive cleaning for mobile sites that often contain lots of clutter */
    const elements = root.querySelectorAll('p, h2, h3');
    const b = Array.from(elements)
        .filter(el => {
            const s = window.getComputedStyle(el);
            return s.display !== 'none' && s.visibility !== 'hidden' && el.innerText.trim().length > 30;
        })
        .map(el => el.innerText.trim())
        .join('\n\n');

    if(b.length < 100) { alert('Content is too short.'); return; }

    fetch('https://<your-pythonanywhere-domain>.pythonanywhere.com/send', {
        method: 'POST',
        mode: 'cors', /* Important for mobile browsers */
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title: t, body: b})
    })
    .then(r => r.ok ? alert('OK: ' + t) : alert('Error: ' + r.status))
    .catch(e => alert('Failed: ' + e));
})();
```

4.  To use it, open a webpage, tap the address bar, type "Send to Kindle", and tap the bookmark suggestion.
