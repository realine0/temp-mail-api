"""Command-line interface for temp-mail-api."""

from __future__ import annotations

import argparse
from pathlib import Path

from temp_mail_api.checker import EmailChecker


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate email lists and detect disposable addresses.",
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
    args = parse_args()
    input_file = args.input_file.expanduser().resolve()
    output_file = args.output.expanduser().resolve()

    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return 1

    checker = EmailChecker(timeout=args.timeout, delay=args.delay)
    checker.check_file(input_file, output_file)
    print(f"Results written to: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
