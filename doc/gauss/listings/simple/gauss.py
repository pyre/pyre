#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

# get access to the random munber generator functions
import random
# sample size
N = 10**6
# initialize the counters
total = 0
interior = 0
# integrate by sampling some number of times
while total < N:
    # get a random point
    x = random.random()
    y = random.random()
    # check whether it is inside the unit quarter circle
    if (x*x + y*y) <= 1.0: # no need to waste time computing the sqrt
        # update the interior point counter
        interior += 1
    # update the total number points
    total += 1
# print the result:
print("pi: {0:.8f}".format(4*interior/total))

# end of file 
