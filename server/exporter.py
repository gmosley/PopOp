# This file needs to be run from the server/ directory

import csv
import database
from models import ImageSet, Image, Job, Result, User

def export_results():
    results = Result.query.all()
    with open('results.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['id', 'set_id', 'worker_id', 'description', 'first', 'second', 'third', 'first_addr', 'second_addr', 'third_addr'])
        for row in results:
            description = ImageSet.query.with_entities(ImageSet.description).filter(ImageSet.id == row.set_id).first()[0]
            first = Image.query.with_entities(Image.id, Image.address).filter(Image.address == row.first).first()
            second = Image.query.with_entities(Image.id, Image.address).filter(Image.address == row.second).first()
            third = Image.query.with_entities(Image.id, Image.address).filter(Image.address == row.third).first()
            csvwriter.writerow([row.id, row.set_id, row.worker_id, description, first[0], second[0], third[0], first[1], second[1], third[1]])

export_results()