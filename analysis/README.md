# Analysis

### Generating pagerank of image sets

To generate aggregated results of image sets run `python exporter.py` inside of the /server directory. Then move `results.csv` into /analysis and run: `python pagerank.py`.

To generate an html chart out of the pagerank results make sure you ran `pageRank.py` in the previous step and run `python generate_chart.py`. The output file will be named `aggregate_chart.html`.


### Generating the 'Individual Agreement with Aggregated Results by Topic' chart

We first want to use the Alchemy API taxonomy endpoint to categorize each image set desciption. We do this by running 
```
python taxonomy.py imagesets.csv taxonomy_json.csv
``` 
The first argument is the imageset csv, and the second argument is the name of the csv to output.

Next we want to generate topic to judgement-agreement data (this one was fun): 
```
python taxonomy_parser.py taxonomy_json.csv final_rankings.csv 
  results.csv > agreements.txt
``` 
We've charted out our results in `label_agreement.html`
