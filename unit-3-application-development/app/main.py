"""
Enterprise Student Record & Academic Management Platform
Application Entrypoint & Factory Wrapper.
Authored by Om Tambe (PRN: 2125UMLM1065) - Sandip University.
"""

import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
