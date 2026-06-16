"""
run.py — One-click launcher for the AI Cold Email Generator.

Just run:   python run.py
"""

import subprocess
import sys
import os

def main():
    # Path to main.py relative to this file
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "main.py")

    print("=" * 55)
    print("  ✉️  AI Cold Email Generator")
    print("  Starting Streamlit app...")
    print("=" * 55)
    print()

    try:
        subprocess.run(
            [
                sys.executable, "-m", "streamlit", "run", app_path,
                "--server.headless", "false",
                "--browser.gatherUsageStats", "false",
            ],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n\nApp stopped.")
    except FileNotFoundError:
        print("ERROR: streamlit not found. Run:  pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
