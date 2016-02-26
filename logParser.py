import gzip
import os
import traceback
from datetime import datetime


class LogParser:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.zipped_files = []
        self.data = []
        self.primary_lines = []
        self.dates = []
        self.bins = [0]*29
        self.acceptable_exts = {'log'}

    def fill_files(self):
        files = os.listdir(self.dir_path)
        for file in files:
            ext = self.get_extension(file, '.')
            if not ext:
                ext = self.get_extension(file, '_')
            if ext and ext == 'gz':
                data = self.unzip_file(os.path.join(self.dir_path, file))
                self.data.append(data)
            elif ext:
                is_int = True
                try:
                    int(ext)
                except ValueError:
                    is_int = False
                if is_int or ext in self.acceptable_exts:
                    with open(os.path.join(self.dir_path, file)) as log_file:
                        data = log_file.read()
                        self.data.append(data)
                    log_file.close()
        return None

    def unzip_file(self, file_path):
        try:
            with gzip.open(file_path, 'r') as zipped_file:
                data = zipped_file.read()
            zipped_file.close()
            return data.decode(encoding='UTF-8',errors='strict')
        except Exception as e:
            traceback.print_exc()

    def get_primary_lines(self):
        for datum in self.data:
            try:
                lines = datum.split('- -')
                self.primary_lines += [line for line in lines if 'app.js' in line]
            except:
                print('error with: ', datum)
        return None

    def get_extension(self, file_name, punctuation):
        parts = file_name.split(punctuation)
        if len(parts) == 1:
            return None
        return parts[len(parts) - 1]

    def fill_dates(self):
        self.dates = [self.get_date_from_line(line) for line in self.primary_lines]
        return None

    def get_date_from_line(self, line):
        start = line.find('[')
        end = line.find('+')
        date_string = line[start + 1:end - 1]
        return datetime.strptime(date_string, '%d/%b/%Y:%H:%M:%S')

    def fill_bins(self):
        for date in self.dates:
            hits = self.bins[date.day - 1]
            self.bins[date.day -1] = hits + 1
        return None
