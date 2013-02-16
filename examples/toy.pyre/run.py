#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#

# get the toys
import toy

# driver
def test():
    
    # create a person
    alec = toy.student(name='alec')
    activities = tuple(alec.perform())
    assert activities == (
        'studying for 2.0 hours', 'relaxing for 3.0 hours',
        'studying for 1.0 hour', 'relaxing for 1.0 hour'
        )

    # and another one
    joe = toy.policeman(name='joe')
    activities = tuple(joe.perform())
    assert activities == ('patrolling for 5.0 hours', 'relaxing for 1.5 hours')

    return


# main
if __name__ == "__main__":
    test()


# end of file 
