# Temp Mail API

Temp Mail API is a small Python CLI for validating email lists and identifying disposable or temporary mail addresses. It is useful for QA, signup-flow testing, lead-list hygiene, and automation pipelines that need a lightweight email status report.

## Features

- Checks one email per line from a text file
- Reports status, mailbox type, disposable flag, and avatar presence
- Uses checkpoint files so large runs can resume safely
- Retries transient network failures and basic rate-limit responses
- Writes a human-readable results report
- Keeps credentials, sessions, request captures, and generated data out of the repository

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
temp-mail-check examples/emails.txt
```

Write to a custom report path:

```bash
temp-mail-check examples/emails.txt --output reports/results.txt
```

Tune request behavior:

```bash
temp-mail-check examples/emails.txt --timeout 15 --delay 2
```

## Output

The report includes separate sections for valid emails, invalid emails, and request errors. During a run, a checkpoint file is created next to the input file, for example:

```text
examples/emails.txt.checkpoint
```

Run the same command again to continue from where the previous run stopped.

## Responsible Use

This project is intended for legitimate testing, QA, and email-list validation. It does not include credential stuffing, CAPTCHA solving, session capture, account automation, or provider bypass logic.

## License

MIT
