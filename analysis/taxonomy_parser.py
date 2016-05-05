import sys
import json
import csv
from pprint import pprint
import operator

if(len(sys.argv) != 4):
	sys.stderr.write('needs 3 input args\n')
	exit(1)

labelFile= sys.argv[1]
prFile = sys.argv[2]
ratingFile = sys.argv[3]

labelsCsv = csv.reader(open(labelFile, 'rb'))
pageRankCsv = csv.reader(open(prFile, 'rb'))
ratingsCsv = csv.reader(open(ratingFile, 'rb'))

# what are the ids associated with each label
ids_by_label = {}

for row in labelsCsv :
	if row[1] == 'description' : continue
	result = json.loads(row[2].encode('utf-8'))
	if len(result) == 0 :
		continue;

	label = result[0]['label'].split('/')[1]
	set_id = row[0];

	if label not in ids_by_label :
		ids_by_label[label] = []

	ids_by_label[label].append(set_id)


# what are the calculated page ranks for each set_id
page_ranks_by_set_id = {}

for row in pageRankCsv :
	if row[0] == 'set_id': continue

	set_id = row[0]
	pageRanks = json.loads(row[2]);

	page_ranks_by_set_id[set_id] = pageRanks


# what are the rankings corresponding to each set id
rankings_by_set_id = {}

for row in ratingsCsv:
	if row[0] == 'id': continue

	set_id = row[1]
	worker_id = row[2]
	first = row[4]
	second = row[5]
	third = row[6]

	if set_id not in rankings_by_set_id :
		rankings_by_set_id[set_id] = []

	rankings_by_set_id[set_id].append([first, second, third])


# how many pairwise comparisons agree for each ranking in each image set
agreements_by_set_id = {}

for set_id in rankings_by_set_id :
	all_rankings = rankings_by_set_id[set_id]
	agreements_by_set_id[set_id] = []
	page_ranks = page_ranks_by_set_id[set_id]

	page_ranks = sorted(page_ranks, key=operator.itemgetter(2), reverse=True)

	for ranking in all_rankings :
		value = 0

		index = 0

		for data in page_ranks:
			if data[0]   == ranking[0]: first  = index
			elif data[0] == ranking[1]: second = index
			elif data[0] == ranking[2]: third  = index

			index += 1

		if first < second: value += 1
		if second < third: value += 1
		if first  < third: value += 1

		agreements_by_set_id[set_id].append(value)

# what is the percent of pairwise comparisons that agree
agreement_by_label = {}

# decided to average all of the ratings rather than the average rating per image set
for label in ids_by_label :
	total_true = 0
	total = 0

	for set_id in ids_by_label[label] :
		agreements = agreements_by_set_id[set_id]
		total_true += sum(agreements)
		total += len(agreements)

	agreement_by_label[label] = total_true, 3 * total - total_true

for label in agreement_by_label:
	print "['" + label.encode('utf-8') + "', " + \
	str(agreement_by_label[label][0]) + ', ' + \
	str(agreement_by_label[label][1]) + '],'