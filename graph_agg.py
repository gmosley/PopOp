import numpy as np
import math

if __name__ == "__main__":

  # assuming input will come in row by row of format "worse, better"
  inputs = [[0, 1], [1, 2], [0, 1], [0, 1], [1, 2], [2, 1], [0, 2], [2,0], [0,2]]
  # also assuming we have some input telling us how many pictures there are to be sorted
  n = 3

  # initialize n by n array
  a = []
  for _ in xrange(0,n):
    a.append([0.0] * n)
  # a = [[1,2,3],[4,5,6],[7,8,9]]
  for inp in inputs:
    a[inp[0]][inp[1]] += 1
  print a

  for i in xrange(0, n):
    s = 0
    for j in xrange(0,n):
      s += a[j][i]
    for j in xrange(0,n):
      a[j][i] /= s
  A = np.matrix(a)
  print A

  # since our graphs almost always have less than say 20 nodes, we can easily 
  # calculate page rank after the i'th iteration by simply doing the following
  # make a vector of weights adding to 1
  v = []
  for i in range(0,n):
    v.append([1.0/n])
  v = np.matrix(v)
  print v

  # get rankings after 10 iterations
  rankings = np.linalg.matrix_power(A, 10)*v
  print "10 iterations:"
  print rankings

  rankings = np.linalg.matrix_power(A, 50)*v
  print "50 iterations:"
  print rankings

  rankings = np.linalg.matrix_power(A, 100)*v
  print "100 iterations:"
  print rankings

  rankings = np.linalg.matrix_power(A, 300)*v
  print "300 iterations:"
  print rankings