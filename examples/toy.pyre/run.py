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
    
    alec = toy.student(name='alec')
    # print(alec.pyre_nameserver.dump('alec'))
    # print(alec.pyre_nameserver['toy.people.student.activities'])
    # print(alec.pyre_nameserver['alec.activities'])
    # print(alec.pyre_nameserver['alec.foo'])
    activities = tuple(alec.perform())
    assert activities == (
        'studying for 2.0 hour', 'relaxing for 1.0 hour', 'studying for 1.0 hour'
        )

    joe = toy.policeman(name='joe')
    activities = tuple(joe.perform())
    assert activities == ('patrolling for 5.0 hour', 'relaxing for 1.5 hour')

    return


# main
if __name__ == "__main__":
    test()


# end of file 
