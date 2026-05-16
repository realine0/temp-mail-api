"""Backward-compatible command-line shortcut."""

from __future__ import annotations

import argparse
from pathlib import Path

from temp_mail_api.cli import run_check_list


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="temp-mail-check",
        description="Validate an email list and detect disposable addresses.",
    )
    parser.add_argument("input_file", type=Path, help="Text file with one email per line")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("results.txt"),
        help="Where to write the validation report",
    )
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between checks")
    return parser.parse_args()


def main() -> int:
    return run_check_list(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
