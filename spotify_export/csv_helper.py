import csv

def open_csv(filename, newline='', encoding=None):
    with open('chart.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        result = []
        
        title=list(next(reader))
        
        return result
