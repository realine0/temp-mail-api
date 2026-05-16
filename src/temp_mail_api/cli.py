"""Command-line interface for temp-mail-api."""

from __future__ import annotations

import argparse
from pathlib import Path

from temp_mail_api.checker import EmailChecker


def add_check_list_parser(subparsers: argparse._SubParsersAction) -> None:
    check_parser = subparsers.add_parser(
        "check-list",
        help="Validate an email list and detect disposable addresses",
    )
    check_parser.add_argument("input_file", type=Path, help="Text file with one email per line")
    check_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("results.txt"),
        help="Where to write the validation report",
    )
    check_parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds")
    check_parser.add_argument("--delay", type=float, default=1.5, help="Delay between checks")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="temp-mail-api",
        description="Temp mail API toolkit for disposable inbox testing and email validation.",
    )
    subparsers = parser.add_subparsers(dest="command")
    add_check_list_parser(subparsers)

    parser.epilog = (
        "Examples:\n"
        "  temp-mail-api check-list examples/emails.txt\n"
        "  temp-mail-check examples/emails.txt --output results.txt"
    )
    return parser.parse_args()


def run_check_list(args: argparse.Namespace) -> int:
    input_file = args.input_file.expanduser().resolve()
    output_file = args.output.expanduser().resolve()

    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return 1

    checker = EmailChecker(timeout=args.timeout, delay=args.delay)
    checker.check_file(input_file, output_file)
    print(f"Results written to: {output_file}")
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "check-list":
        return run_check_list(args)

    return legacy_main(args)


def legacy_main(args: argparse.Namespace) -> int:
    """Keep the old temp-mail-check script ergonomic."""
    if hasattr(args, "input_file"):
        return run_check_list(args)

    print("Run `temp-mail-api check-list examples/emails.txt` to validate an email list.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
