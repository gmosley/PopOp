import numpy as np
from scipy.sparse import csc_matrix

import database
from models import ImageSet, Result, Image

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

def pageRankForSet(set_id):
    i = 0
    nodes = {}
    nodes_inverse = {}
    images = Image.query.with_entities(Image.address).filter(Image.set_id == set_id).all()
    imgs = []
    for a in images:
        imgs.append(a[0])
    results = Result.query.filter(Result.set_id == set_id).all()
    parsed_results = []
    for r in results:
        if r.first not in imgs or r.second not in imgs or r.third not in imgs:
            print "Invalid result"
            continue
        parsed_results.append(r)
        if r.first not in nodes:
            nodes[r.first] = i
            nodes_inverse[i] = r.first
            i += 1
        if r.second not in nodes:
            nodes[r.second] = i
            nodes_inverse[i] = r.second
            i += 1
        if r.third not in nodes:
            nodes[r.third] = i
            nodes_inverse[i] = r.third
            i += 1
    a = []
    n = len(nodes)
    for _ in xrange(0,n):
        a.append([0.0] * n)
    for r in parsed_results:
        a[nodes[r.second]][nodes[r.first]] += 1
        a[nodes[r.third]][nodes[r.second]] += 1
        # a[nodes[r.third]][nodes[r.first]] += 1
    A = np.matrix(a)
    rankings = pageRank(A, 0.86)
    results = []
    # print rankings
    for r in xrange(0, len(rankings)):
        results.append((rankings[r], nodes_inverse[r]))
    results.sort(key=lambda tup: tup[0], reverse=True)

    rankings = []
    for i in results:
        rankings.append(i[1])

    # calculate agreement
    agreements = 0
    total = len(parsed_results) * 2
    for r in parsed_results:
        first = rankings.index(r.first)
        second = rankings.index(r.second)
        third = rankings.index(r.third)
        if first < second: agreements += 1
        if second < third: agreements += 1
        # if first < third: agreements += 1

    agree = int(float(agreements)/total * 100)
    return results, agree
print pageRankForSet(3)