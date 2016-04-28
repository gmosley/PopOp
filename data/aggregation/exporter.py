import sys
import csv
sys.path.append('../../server')
import database
from models import ImageSet, Image, Job, Result, User

def export_results:
  results = Result.query.with_entities(Image.id).all()
  with open('results.csv', 'wb') as mycsvfile:
    for row in result:
        print(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3]+ "\t"+row[4]+"\t"+row[5])
