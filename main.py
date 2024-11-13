import logging
import os
from flask import Flask, render_template, send_from_directory
from gunicorn.app.base import BaseApplication

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

# Configure static file serving for production
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/")
def home_route():
    return render_template("home.html")

@app.route("/backup")
def backup_route():
    # Implement backup logic to store the table data for 24 hours
    # TODO: Implement actual backup logic
    return "Backup functionality not yet implemented. This feature is under construction."

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        # Apply configuration to Gunicorn
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    options = {
        "bind": f"0.0.0.0:{port}",
        "workers": 4,
        "loglevel": "info",
        "accesslog": "-"
    }
    StandaloneApplication(app, options).run()