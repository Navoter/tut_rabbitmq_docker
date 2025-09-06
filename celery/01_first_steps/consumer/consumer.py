#!/usr/bin/env python
import time
import sys
from worker import add

TIMEOUT = 30

if __name__ == "__main__":
    i=0
    while True:
        result = add.delay(i, 1000)
        print(f'Task submitted. Task ID: {result.id}', file=sys.stderr)
        try:
            # value = result.get(timeout=2)
            value = result
            print(f'Task result: {value}', file=sys.stderr)
        except Exception as e:
            print(f'Error getting result: {e}', file=sys.stderr)
        print(f'Waiting {TIMEOUT} seconds before next task...', file=sys.stderr)
        time.sleep(TIMEOUT)
        i=i+1