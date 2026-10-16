# Log analysis starter

A small command-line parser for a specific CSV-like log format: `timestamp,user,action`. It prints the three fields and reports malformed rows. This is a parsing example; anomaly detection and support for other log formats are not implemented.

## Quick start

Requires Python 3.11 or later. Uses only the standard library.

```bash
git clone https://github.com/Hellfire4959/Log-analysis-tool.git
cd Log-analysis-tool
python scripts/parse_logs.py examples/sample.log
```

To read another file:

```bash
python scripts/parse_logs.py path/to/events.log
```

## Input and output

Input is UTF-8 CSV **without a header**, with exactly three fields per record. Quoted commas are supported:

```csv
2026-10-16T09:00:00Z,alex,login_success
2026-10-16T09:05:00Z,sam,"export, report"
```

Parsed entries are printed to standard output. The summary and diagnostics go to standard error. Blank rows are ignored; rows with the wrong field count are skipped with their line number. Invalid CSV syntax or an unreadable file ends the command.

| Exit code | Meaning |
| --- | --- |
| `0` | Parsed without malformed rows |
| `1` | File, encoding, or CSV syntax error |
| `2` | At least one row had the wrong field count, or command-line usage was invalid |

## Layout and extending it

- [scripts/parse_logs.py](scripts/parse_logs.py) — parser and CLI; replaces the original extensionless `Python code to parse log files`.
- [examples/sample.log](examples/sample.log) — synthetic, headerless sample.
- [tests/](tests/) — quoted-field, malformed-row and file-error coverage.

```bash
python -m unittest discover -s tests -v
```

To support Apache, Windows events, JSON logs or a different schema, add a dedicated parser and a representative synthetic fixture. Timestamp validation, event correlation and anomaly rules would be separate features.
