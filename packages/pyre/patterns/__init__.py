# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
This package contains functions and classes that encapsulate common usage patterns.
"""


# external packages
import itertools, collections


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

    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


# autovivified maps
def vivify(levels=1, atom=dict):
    """
    Builds a nested {defaultdict} with a fixed depth and a specified type at the deepest level.

    Adopted from (http://en.wikipedia.org/wiki/Autovivification)
    """
    # the embryonic case is a {defaultdict} of type {atom}
    if levels < 2: return collections.defaultdict(atom)
    # otherwise, build a {defaultdict} that is shallower by one level
    return collections.defaultdict(lambda: vivify(levels=levels-1, atom=atom))


# factories
def newPathHash(**kwds):
    """
    Build a hashing functor for name hierarchies
    """
    from .PathHash import PathHash
    return PathHash(**kwds)


# end of file 
