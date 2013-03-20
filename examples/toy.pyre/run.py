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

    # startup stuff
    # print("person.friends:\n  {}\n  {}".format(toy.person.friends, type(toy.person.friends)))
    # print("student.friends:\n  {}\n  {}".format(toy.student.friends, type(toy.student.friends)))
    
    michael = toy.person(name='michael')
    # here is a generic student
    jane = toy.student(name='jane')
    jane.activities = toy.relax, 'study#math', '#physics'
    activities = tuple(jane.perform())
    assert activities == (
        'relaxing for 1.0 hour', 'studying for 1.0 hour', 'studying for 2.0 hours'
        )
    assert jane.friends['teacher'] is michael

    # create persons named in the configuration file
    alec = toy.student(name='alec')
    activities = tuple(alec.perform())
    assert activities == (
        'studying for 2.0 hours', 'relaxing for 3.0 hours',
        'studying for 1.0 hour', 'relaxing for 1.0 hour'
        )
    # print(alec.friends['girlfriend'].pyre_name)
    # print(alec.friends['girlfriend'].friends)
    assert alec.friends['teacher'] is michael

    jessica = toy.student(name='jessica')
    activities = tuple(jessica.perform())
    assert activities == (
        'studying for 0.5 hours', 'relaxing for 3.0 hours',
        'studying for 1.5 hours', 'relaxing for 1.0 hour'
        )
    # print(jessica.friends)
    assert jessica.friends['teacher'] is michael

    # check the relationships
    assert alec.friends['girlfriend'] is jessica
    assert jessica.friends['boyfriend'] is alec

    joe = toy.policeman(name='joe')
    activities = tuple(joe.perform())
    assert activities == ('patrolling for 5.0 hours', 'relaxing for 1.5 hours')

    # augment some relationships
    alec.friends.update({'joe': "#joe"})
    alec.friends['joe'] is joe
 
    # show me
    # print("person.friends:\n  {}\n  {}".format(toy.person.friends, type(toy.person.friends)))
    # print("student.friends:\n  {}\n  {}".format(toy.student.friends, type(toy.student.friends)))
    # print("alec.friends:\n  {}\n  {}".format(alec.friends, type(alec.friends)))
    # print("jessica.friends:\n  {}\n  {}".format(jessica.friends, type(jessica.friends)))

    # all done
    return jane, alec, jessica, joe


# main
if __name__ == "__main__":
    test()


# end of file 
