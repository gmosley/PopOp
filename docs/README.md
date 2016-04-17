PopOp
=====

Intro
-----
PopOp will take the form of a web app. Users will be able to post a set of images and a ranking criteria. Other contributors will vote on the best image based on the given criteria.

Components
----------
* Server
 - We will use node.js with the express framework (4 points)
* Database
 - User information (including rankings) will be stored in Redis or a SQL database. (4 points)
 - Images will probably be stored on Amazon S3. (3 points)
* Contributor Interface
 - Contributors will be presented with a set of images and a ranking criteria in HIT like fashion. Users will arrange the images based on the criteria. This will be accomplished in pure javascript. (3 points)
* Requestor Interface
 - Requestors will be asked to upload a set of images and enter their criteria. (3 points)
 
QC
--
Our biggest concern regarding quality control is if the user submits inappropriate photos. In regards to this, we have determined that a major component of these photos would concern nuidty. Screening such photos is done through a module that we have downloaded online, called nude.py. This functions as a Python port to nude.js. 

Aggregation
-----------
Aggregation and analysis of data is done using a directed graph. Each individual vertex in the graph represents a particular image, and each edge represents a comparison between two different images. A -> B would represent A < B in terms of comparisons. In order to find which image is ranked the highest, we would perform PageRank over the graph. 
 
