import csv
import database
from models import ImageSet, Image, Job, Result, User

outfile = open('results.csv', 'wb')
outcsv = csv.writer(outfile)
records = session.query(ImageSet).all()
[outcsv.writerow([getattr(curr, column.name) for column in ImageSet.__mapper__.columns]) for curr in records]
# or maybe use outcsv.writerows(records)

outfile.close()
