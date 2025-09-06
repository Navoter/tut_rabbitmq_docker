#!/usr/bin/env python3
import sys
import platform
import time

def main():
    # Try to get the Pika version
    try:
        import pika
        pika_version = pika.__version__
    except ImportError:
        pika_version = "not installed"

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
    print(f"Pika version: {pika_version}", file=sys.stderr)
    print("Application is running successfully!", file=sys.stderr)
    print("Container will be shutting down in 30 seconds.", file=sys.stderr)
    time.sleep(10)

if __name__ == "__main__":
    main()