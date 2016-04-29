import jinja2
import csv
import json
import operator


env = jinja2.Environment(loader = jinja2.FileSystemLoader('.'))
template = env.get_template('chart_template.html')

data = []

with open('final_rankings.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        rankings = {}
        for (_, img_url, score) in json.loads(row['result']):
            rankings[img_url] = score
        sorted_rankings = sorted(rankings.items(), key=operator.itemgetter(1), reverse=True)
        data.append({ 'description': row['description'], 'images': sorted_rankings})


with open('aggregate_chart.html', 'w') as out:
    out.write(template.render(data=data))

# >>> template = Template('Hello {{ name }}!')
# >>> template.render(name='John Doe')