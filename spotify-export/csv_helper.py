import csv

def open_csv(filename, newline='', encoding=None):
    with open(filename, newline=newline, encoding=encoding) as f:
        reader = csv.reader(f)
        return list(reader)
