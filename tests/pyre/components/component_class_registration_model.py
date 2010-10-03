#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise component registration
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

    # fetch the configurator
    conf = pyre.executive.configurator
    # and the model
    model = conf.model
    # model.dump()

    # print(" -- making some configuration changes")
    # add an assignment
    model['test.p1'] = 'step 1'
    # an alias
    model.alias(alias='p1', canonical='test.p1')
    # and a reference to the alias
    model['ref'] = '{p1}'
    # check that they point to the same slot
    assert model['p1'] == model['test.p1']
    # save the nodes
    ref = model['ref']
    step_0 = model['test.p1']
    # print("original node:", step_0)
    # print("    _value: {._value!r}".format(step_0))
    # print("    _evaluator: {._evaluator!r}".format(step_0))
    # print("    _priority: {._priority!r}".format(step_0))
    # model.dump()
    # print(" -- done")

    # now declare the component and its interface
    # print(" -- declaring components")
    component = declare()
    # print(" -- done")
    assert component.p1 == 'step 1'
    assert component.p2 == 'p2'
    # grab the component parts
    inventory = component.pyre_inventory
    p1slot = inventory[component.pyre_getTraitDescriptor(alias='p1')]
    # print("slot: component.p1:", p1slot)
    # print("    _value: {._value!r}".format(p1slot))
    # print("    _evaluator: {._evaluator!r}".format(p1slot))
    # print("    _priority: {._priority!r}".format(p1slot))
    p2slot = inventory[component.pyre_getTraitDescriptor(alias='p2')]
    # print("slot: component.p2:", p2slot)
    # print("    _value: {._value!r}".format(p2slot))
    # print("    _evaluator: {._evaluator!r}".format(p2slot))
    # print("    _priority: {._priority!r}".format(p2slot))

    # check that the model is as we expect
    # model.dump()
    assert model['test.p1'] == p1slot
    assert model['test.p2'] == p2slot
    # how about the alias and the reference?
    assert model['ref'].value == component.p1
    assert model['p1'].value == component.p1

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
