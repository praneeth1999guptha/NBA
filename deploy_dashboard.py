#!/usr/bin/env python3
"""Serve nba_dashboard.html locally and automatically open it in a browser.

Usage:
    python deploy_dashboard.py [--port 8080] [path/to/nba_dashboard.html]

If you omit the path, the script looks for `nba_dashboard.html` in the
current working directory.
"""

import http.server
import socketserver
import argparse
import webbrowser
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(description="Serve a static HTML dashboard.")
    parser.add_argument("html", nargs="?", default="nba_dashboard.html",
                        help="Path to nba_dashboard.html (default: ./nba_dashboard.html)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port to host on (default: 8000)")
    args = parser.parse_args()

    html_path = Path(args.html).resolve()
    if not html_path.exists():
        sys.exit(f"✖ File not found: {html_path}")

    # Change directory so the HTTP server serves the file's folder
    os.chdir(html_path.parent)

    class Handler(http.server.SimpleHTTPRequestHandler):
        # Serve files from the directory containing the HTML
        def __init__(self, *handler_args, **handler_kwargs):
            super().__init__(*handler_args, directory=str(html_path.parent), **handler_kwargs)

    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        url = f"http://localhost:{args.port}/{html_path.name}"
        print(f"✔ Serving {url}
Press Ctrl+C to stop.")
        try:
            # Open the dashboard in the default browser
            webbrowser.open_new_tab(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("
✖ Stopping server…")

if __name__ == "__main__":
    import os
    main()
