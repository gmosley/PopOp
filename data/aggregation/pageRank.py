import csv

set_ids_to_results = {}

with open('results.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    set_id = -1

    for row in reader:
        fst = row['first']
        snd = row['second']
        thd = row['third']
    	if (set_id != row['set_id']):
    		set_id = row['set_id']
    		set_ids_to_results[set_id] = [];
  		set_ids_to_results[set_id].append((first, second, third))

        worker_id = row['worker_id']