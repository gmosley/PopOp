import urllib2
import urllib
import json 
import csv
import sys

#TODO fill in your own API key
api_key = '74a3ce694c1052de5ee0b55a17567c14aa234dc1'

if(len(sys.argv) != 3):
  sys.stderr.write('needs input and output args\n')
  exit(1)

inputfile = sys.argv[1]
outputfile = sys.argv[2]

def construct_api_call(text):
  ending = urllib.urlencode({'apikey' : api_key, 'text': text, 'outputMode': 'json'})
  return "http://gateway-a.watsonplatform.net/calls/text/TextGetRankedTaxonomy?" + ending

def get_taxonomy(text) : 
  try: 
    output = urllib2.urlopen(construct_api_call(text))
  except urllib2.HTTPError: 
    sys.stderr.write('BAD REQUEST\n')
    return None
  try:
    response = json.loads(output.read())
  except ValueError:
    sys.stderr.write('JSON ERROR\n')
    return None
  sys.stderr.write('%s\t%s\n'%(response['status'], text))
  if response['status'] == 'OK' :
    return response['taxonomy']
  return None

csvReader = csv.reader(open(inputfile, 'rb'))
output = csv.writer(open(outputfile, 'w'))

output.writerow(['id', 'description', 'json'])

for row in csvReader :
  if(row[2] == 'description'): continue
  result = get_taxonomy(row[2])
  output.writerow([row[0], row[2], result])
  # break
  # if(result == None) :
  #   continue;
  # # print row[0], row[2], result[0]['label'];
  # break;