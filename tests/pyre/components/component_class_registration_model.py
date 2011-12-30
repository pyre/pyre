#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that component registration interacts correctly with the pyre configurator model
"""

# access
# print(" -- importing pyre")
import pyre
# print(" -- done")


def declare():

    # declare an interface
    class interface(pyre.interface):
        """an interface"""
        # properties
        p1 = pyre.properties.str()
        p2 = pyre.properties.str()
        # behavior
        @pyre.provides
        def do(self):
            """behave"""
        
    # declare a component
    class component(pyre.component, family="test", implements=interface):
        """a component"""
        # traits
        p1 = pyre.properties.str(default="p1")
        p2 = pyre.properties.str(default="p2")

        @pyre.export
        def do(self):
            """behave"""
            return "component"

    return component


def test():

    # and the model
    model = pyre.executive.configurator
    # model.dump()

    # print(" -- making some configuration changes")
    # add an assignment
    model['test.p1'] = 'step 1'
    # an alias
    model.alias(alias='p1', canonical='test.p1')
    # and a reference to the alias
    model['ref'] = '{p1}'
    # check that they point to the same slot
    assert model._resolve(name='p1') == model._resolve(name='test.p1')
    # save the nodes
    ref = model._resolve(name='ref')
    step_0 = model._resolve(name='test.p1')

    # now declare the component and its interface
    # print(" -- declaring components")
    component = declare()
    # print(" -- done")
    assert component.p1 == 'step 1'
    assert component.p2 == 'p2'
    # grab the component parts
    inventory = component.pyre_inventory
    p1slot = inventory[component.pyre_getTraitDescriptor(alias='p1')]
    p2slot = inventory[component.pyre_getTraitDescriptor(alias='p2')]

    # check that the model is as we expect
    # model.dump()
    p1node,_ = model._resolve(name='test.p1')
    assert p1node == p1slot
    p2node,_ = model._resolve(name='test.p2')
    assert p2node == p2slot
    # how about the alias and the reference?
    assert model['ref'] == component.p1
    assert model['p1'] == component.p1

    # finally, make a late registration to what is now the component trait
    model['test.p2'] = 'step 2'
    # and check
    assert component.p1 == 'step 1'
    assert component.p2 == 'step 2'

    return

     

# main
if __name__ == "__main__":
    test()


# end of file 
