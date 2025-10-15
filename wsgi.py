"""
WSGI config for EmotionFAD.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments.
"""

import os
from app_emotion import app, socketio

# This application object is used by any WSGI server configured to use this file.
application = app

def run():
    """Run the application"""
    port = int(os.environ.get('PORT', 5000))
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development',
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )

if __name__ == "__main__":
    run()
