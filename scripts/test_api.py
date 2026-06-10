"""System health testing script for validating localized deployment builds."""

import sys
import requests

def run_smoke_test():
    """Runs a quick live environment smoke test to verify backend health and routes."""
    target_host = "http://127.0.0.1:8000"
    print(f"Connecting to runtime target environment at: {target_host}...")
    try:
        response = requests.get(f"{target_host}/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("🚀 Live application smoke test complete. System is functional!")
            sys.exit(0)
        print(f"Unexpected response payload signature returned: {response.text}")
        sys.exit(1)
    except Exception as err:
        print(f"Failed to connect to the target server instance: {str(err)}")
        sys.exit(1)

if __name__ == "__main__":
    run_smoke_test()