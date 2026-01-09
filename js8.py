"""Simple JS8Call monitor script.

Provides a small CLI that starts a headless JS8Call client, logs
incoming messages and can set the operating frequency.
"""

import sys
import datetime
import time
import argparse
import os
from pyjs8call import Client

os.environ["QT_QPA_PLATFORM"] = "xcb"
if "WAYLAND_DISPLAY" in os.environ:
    del os.environ["WAYLAND_DISPLAY"]

FREQUENCY_MAP = {
    "std": 7078000,
    "gn": 7107000
}


def rx_callback(msg, log_file=None):
    """Handle an incoming message and optionally log it.

    msg may be None or missing attributes; this function builds a
    safe output string and writes it to the console and/or a log
    file specified by ``log_file``.
    """
    timestamp = time.strftime(
        "%Y-%m-%d %H:%M:%S",
        time.localtime(getattr(msg, "timestamp", time.time())),
    )
    origin = getattr(msg, "origin", "-")
    snr = getattr(msg, "snr", "-")
    text = getattr(msg, "text", "")

    output_str = f"[{timestamp}] {origin} ({snr}dB): {text}"

    # Print to Console if there's text
    if text:
        print(output_str)

    # Log to File if requested
    if log_file:
        try:
            with open(log_file, "a+", encoding="utf-8") as f:
                f.write(output_str + "\n")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[LOG ERROR] Could not write to file: {exc}")


def set_freq(args, js8):
    """Set the JS8Call frequency based on parsed CLI arguments.

    ``args`` is the argparse Namespace containing ``gn`` and ``std``
    boolean flags. ``js8`` is the Client instance to configure.
    """
    if args.gn:
        freq = FREQUENCY_MAP.get('gn')
        if freq:
            print(f"Setting frequency to {freq} Hz")
            js8.settings.set_freq(freq)
    if args.std:
        freq = FREQUENCY_MAP.get('std')
        if freq:
            print(f"Setting frequency to {freq} Hz")
            js8.settings.set_freq(freq)


def main():
    """CLI entrypoint: parse args, start client, and run loop."""

    parser = argparse.ArgumentParser(description="JS8Call Monitor Script")
    parser.add_argument(
        '--gn', action='store_true', help='set the frequency to the ghost net frequency')
    parser.add_argument(
        '--std', action='store_true', help='set the frequency to the standard 40m js8 call freq')
    args = parser.parse_args()

    js8 = Client()

    with open('js8call.log', 'a+', encoding='utf-8') as f:
        now = datetime.datetime.now()
        f.write(f'\n New log starting {now}\n')

    # Assign the callback with the log_file argument baked in
    js8.callback.register_incoming(
        lambda msg: rx_callback(
            msg, log_file='js8call.log'))

    print("Starting engine...")
    try:
        js8.start(headless=True)
        max_retries = 30
        attempts = 0

        while not js8.online and attempts < max_retries:
            print(
                f"Waiting for JS8Call API... (Attempt {attempts + 1}/{max_retries})"
            )
            time.sleep(1)
            attempts += 1

        set_freq(args, js8)
    except Exception as e: # pylint: disable=broad-except
        print(f"Error starting JS8Call: {e}")
        sys.exit(1)

    print("Listening... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        js8.stop()


if __name__ == "__main__":
    main()
