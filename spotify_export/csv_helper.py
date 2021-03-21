import csv

def open_csv(filename, newline='', encoding=None):
    with open('chart.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        result = []
        
        title=list(next(reader))
        for rows in reader:
            result.append({title[i]:rows[i] for i in range(len(title))})
        
        return result
