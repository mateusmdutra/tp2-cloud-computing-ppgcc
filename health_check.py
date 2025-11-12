#!/usr/bin/env python3
"""
healthcheck_poller.py

Usage:
    python3 healthcheck_poller.py https://example.com/health --interval 1 --timeout 5

Press Ctrl+C to stop.
"""

import argparse
import time
import sys
from datetime import datetime

import requests


def poll(url: str, interval: float = 1.0, timeout: float = 5.0):
    print(f"Starting healthcheck poller -> url={url} interval={interval}s timeout={timeout}s")
    try:
        while True:
            start = time.time()
            timestamp = datetime.utcnow().isoformat() + "Z"
            try:
                resp = requests.get(url, timeout=timeout)
                status = resp.status_code
                try:
                    body = resp.json()
                    body_str = repr(body)
                except ValueError:
                    text = resp.text.strip()
                    if len(text) > 1000:
                        body_str = text[:1000] + "...(truncated)"
                    else:
                        body_str = text
                print(f"[{timestamp}] {url} -> {status} | {body_str}")
            except requests.exceptions.RequestException as e:
                print(f"[{timestamp}] {url} -> request error: {e}", file=sys.stderr)

            elapsed = time.time() - start
            sleep_for = interval - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)
    except KeyboardInterrupt:
        print("\nPolling stopped by user.")


def main():
    parser = argparse.ArgumentParser(description="Poll a healthcheck endpoint every N seconds and print the result.")
    parser.add_argument("url", help="URL of the healthcheck endpoint (GET)")
    parser.add_argument("--interval", "-i", type=float, default=1.0, help="Polling interval in seconds (default: 1.0)")
    parser.add_argument("--timeout", "-t", type=float, default=5.0, help="Request timeout in seconds (default: 5.0)")
    args = parser.parse_args()

    poll(args.url, interval=args.interval, timeout=args.timeout)


if __name__ == "__main__":
    main()
