import csv

def open_csv(filename, newline='', encoding=None):
    """Reads an n columns wide, m rows long CSV file beginning with a title
    row, and transforms it into a list of dictionaries representing
    individual records"""

    with open('chart.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        result = []
        
        title=list(next(reader))
        for rows in reader:
            result.append({title[i]:rows[i] for i in range(len(title))})
        
        return result
