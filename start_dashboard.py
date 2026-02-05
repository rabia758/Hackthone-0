#!/usr/bin/env python3
"""
AI Employee Dashboard Startup Script
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("Starting AI Employee Dashboard...")
    print()
    print("Please make sure your AI_Employee_Vault directory is properly configured.")
    print("The dashboard will be available at http://127.0.0.1:5000")
    print()

    try:
        # Run the main application
        result = subprocess.run([sys.executable, "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting dashboard: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDashboard stopped by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()