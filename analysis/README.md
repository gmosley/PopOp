# analysis readme

### generating pagerank of image sets webpage

* To generate aggregated results of image sets
Run exporter.py inside of the /server directory.
Move results.csv into /analysis
Run: python pagerank.py

* To generate a html chart out of the pagerank results
Make sure you ran pageRank.py in the previous step
Run: python /data/aggregation/generate_chart.py
The output file will be named aggregate_chart.html


### generating the google column chart of categories vs worker consensus

* to generate the csv of the json from alchemy from the descriptions in imagesets.csv by image set_id
python taxonomy.py imagesets.csv taxonomy_json.csv

* to generate the label to judgement-agreement data from that json (this one was fun):
Run: python taxonomy_parser.py taxonomy_json.csv final_rankings.csv results.csv > agreements.txt

* chart that uses the information in agreements.txt is in label_agreement.html
