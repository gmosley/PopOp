import sys
import json
import csv


if(len(sys.argv) != 3):
  sys.stderr.write('needs input and output args\n')
  exit(1)

inputfile = sys.argv[1]
outputfile = sys.argv[2]

csvReader = csv.reader(open(inputfile, 'rb'))
output = csv.writer(open(outputfile, 'w'))

output.writerow(['id', 'description', 'category'])

for row in csvReader :
  if row[1] == 'description' : continue
  result = json.loads(row[2].encode('utf-8'))
  if len(result) == 0 :
    continue;
  label = result[0]['label'].split('/')[1]
  output.writerow([row[0], row[1], label])