#!/usr/bin/env python3
import sys
import platform
import time

def main():
    # Try to get the Pika version
    try:
        import celery
        celery_version = celery.__version__
    except ImportError:
        celery_version = "not installed"

    # Try to get a pretty OS name from /etc/os-release
    pretty_name = None
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    pretty_name = line.strip().split("=", 1)[1].strip('"')
                    break
    except Exception:
        pass

    print(f"Python version: {sys.version}", file=sys.stderr)
    if pretty_name:
        print(f"OS version: {pretty_name}", file=sys.stderr)
    else:
        print(f"OS version: {platform.platform()}", file=sys.stderr)
    print(f"Celery version: {celery_version}", file=sys.stderr)
    
    # List installed pip packages using pip freeze
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Installed pip packages:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
    except Exception as e:
        print(f"Could not list pip packages: {e}", file=sys.stderr)

    print("Application is running successfully!", file=sys.stderr)
    print("Container will be shutting down in 10 seconds.", file=sys.stderr)
    time.sleep(10)

if __name__ == "__main__":
    main()