import numpy as np
import math
import csv
import json

import numpy as np
from scipy.sparse import csc_matrix

# taken from https://gist.github.com/diogojc/1338222
def pageRank(G, s = .85, maxiters = 100, maxerr = .001):
    """
    Computes the pagerank for each of the n states.
    Used in webpage ranking and text summarization using unweighted
    or weighted transitions respectively.
    Args
    ----------
    G: matrix representing state transitions
       Gij can be a boolean or non negative real number representing the
       transition weight from state i to j.
    Kwargs
    ----------
    s: probability of following a transition. 1-s probability of teleporting
       to another state. Defaults to 0.85
    maxerr: if the sum of pageranks between iterations is bellow this we will
            have converged. Defaults to 0.001
    """
    n = G.shape[0]

    # transform G into markov matrix M
    M = csc_matrix(G,dtype=np.float)
    rsums = np.array(M.sum(1))[:,0]
    ri, ci = M.nonzero()
    M.data /= rsums[ri]

    # bool array of sink states
    sink = rsums==0

    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    count = 0
    while np.sum(np.abs(r-ro)) > maxerr and count < maxiters:
        ro = r.copy()
        # calculate each pagerank at a time
        for i in xrange(0,n):
            # inlinks of state i
            Ii = np.array(M[:,i].todense())[:,0]
            # account for sink states
            Si = sink / float(n)
            # account for teleportation to state i
            Ti = np.ones(n) / float(n)

            r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )
        count += 1
    # return normalized pagerank
    return r/sum(r)

set_ids_to_results = {}
images_urls = {}

with open('results2.csv', 'rb') as csvfile:
    with open('final_rankings.csv', 'wb') as outputfile:
        csvwriter = csv.writer(outputfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        reader = csv.DictReader(csvfile)

        csvwriter.writerow(['set_id', 'result'])
        set_id = -1

        for row in reader:
            # print row
            fst = row['first']
            snd = row['second']
            thd = row['third']
            if fst not in images_urls:
                images_urls[fst] = row['first_addr']
            if snd not in images_urls:
                images_urls[snd] = row['second_addr']
            if thd not in images_urls:
                images_urls[thd] = row['third_addr']

            if (set_id != row['set_id']):
                set_id = row['set_id']
                set_ids_to_results[set_id] = [];
            set_ids_to_results[set_id].append((fst, snd, thd))

            worker_id = row['worker_id']

        for set_id in set_ids_to_results:
            # get map of all ids for a set
            print "starting for set: " + str(set_id)
            i = 0
            nodes = {}
            nodes_inverse = {}
            for res in set_ids_to_results[set_id]:
                for img_id in res:
                    if img_id not in nodes:
                        nodes[img_id] = i
                        nodes_inverse[i] = img_id
                        i += 1
            # print nodes 
            # init n x n array
            a = []
            n = len(nodes)
            for _ in xrange(0,n):
                a.append([0.0] * n)
            # make matrix
            for res in set_ids_to_results[set_id]:
                a[nodes[res[1]]][nodes[res[0]]] += 1
                a[nodes[res[2]]][nodes[res[0]]] += 1
                a[nodes[res[2]]][nodes[res[1]]] += 1
            A = np.matrix(a)
            print A

            rankings = pageRank(A, 0.86)
            tuples = []
            for r in xrange(0, len(rankings)):
                tuples.append((nodes_inverse[r], images_urls[nodes_inverse[r]], rankings[r]))
            csvwriter.writerow([set_id, json.dumps(tuples)])


