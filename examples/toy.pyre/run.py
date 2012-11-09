#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
    print(activities)

    joe = toy.policeman(name='joe')
    # dump(joe)
    activities = tuple(joe.perform())
    print(activities)

    return


# helper
def dump(entity):
    print('{.pyre_name!r}:'.format(entity))
    print('  inventory: {.pyre_inventory}'.format(entity))
    for trait, key in entity.pyre_inventory.items():
        print('    {}'.format(trait))
        slot, fullname = entity.pyre_nameserver.lookup(key)
        print('      full name: {!r}'.format(fullname))
        print('      slot: {}'.format(slot))
        print('        key: {.key}'.format(slot))
        print('        priority: {.priority}'.format(slot))
        print('        locator: {.locator}'.format(slot))
        print('        converter: {.converter}'.format(slot))
        print('        dirty: {.dirty}'.format(slot))
        print('        cache: {._value!r}'.format(slot))
        print('        value: {}'.format(slot.getValue(configurable=entity)))
        slot, fullname = entity.pyre_nameserver.lookup(key)
        print('      slot: {}'.format(slot))
        print('        key: {.key}'.format(slot))
        print('        priority: {.priority}'.format(slot))
        print('        locator: {.locator}'.format(slot))
        print('        converter: {.converter}'.format(slot))
        print('        cache: {._value!r}'.format(slot))
        print('        dirty: {.dirty}'.format(slot))


# main
if __name__ == "__main__":
    test()


# end of file 
