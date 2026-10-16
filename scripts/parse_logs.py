"""Read headerless timestamp,user,action CSV logs and print their fields."""
import argparse
import csv
from pathlib import Path
import sys

def parse_log_file(log_file_path, output=None, errors=None):
    output = sys.stdout if output is None else output
    errors = sys.stderr if errors is None else errors
    processed = skipped = 0
    with Path(log_file_path).open(encoding='utf-8-sig',newline='') as stream:
        reader = csv.reader(stream,strict=True)
        for row in reader:
            if not row or all(not value.strip() for value in row): continue
            if len(row) != 3:
                print(f'Line {reader.line_num}: expected 3 fields, found {len(row)}; skipped.',file=errors)
                skipped += 1; continue
            timestamp,user,action = [value.strip() for value in row]
            print(f'Timestamp: {timestamp}, User: {user}, Action: {action}',file=output)
            processed += 1
    return processed,skipped

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log_file',type=Path,help='UTF-8 CSV-like log with three fields and no header.')
    args=parser.parse_args(argv)
    try:processed,skipped=parse_log_file(args.log_file)
    except (OSError,csv.Error,UnicodeError) as error:
        print(f'Error: {error}',file=sys.stderr);return 1
    print(f'Parsed {processed} entries; skipped {skipped} malformed rows.',file=sys.stderr)
    return 2 if skipped else 0

if __name__=='__main__':sys.exit(main())
