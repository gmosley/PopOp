import csv
import json

with open('taxonomy_json.csv', 'rb') as taxonomy_data:
    reader = csv.DictReader(taxonomy_data)
    for row in reader:
        categories = json.loads(row['json'])
        for category in categories:
            if float(category['score']) >= 0.5:
                print category['label'].replace("/", " "),