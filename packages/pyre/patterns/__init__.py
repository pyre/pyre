# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
This package contains classes that encapsulate common usage patterns.
"""

# utilities
def average(iterable):
    """
    Compute the average value of the entries in {iterable}
    """
    # initialize the counters
    total = 0
    count = 0
    # loop
    for item in iterable:
        # update the counters
        count += 1
        total += item
    # all done
    return total/count


def powerset(iterable):
    """
    Compute the full power set, i.e. the set of all permutations, of the given iterable.
    For example:
        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    Taken from the python itertools documentation
    """
    from itertools import chain, combinations

    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


# factories
def newPathHash(**kwds):
    """
    Build a hashing functor for name hierarchies
    """
    from .PathHash import PathHash
    return PathHash(**kwds)


# end of file 
