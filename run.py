from logParser import LogParser
import sys
import os

try:
    path = sys.argv.pop()
    if not os.path.exists(path):
        sys.exit('Enter a directory where the log files live')
except IndexError:
    sys.exit('No arguments given. Must include a log file path')

log_parser = LogParser(path)
log_parser.fill_files()
log_parser.get_primary_lines()
log_parser.fill_dates()
print('number of entries:', len(log_parser.dates))
log_parser.fill_bins()
for i in range(len(log_parser.bins)):
    print(i + 1, ':', log_parser.bins[i])