# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


"""
Support for workflows
"""

# framework
import pyre

# the protocols
from .Producer import Producer as producer
from .Specification import Specification as specification
from .Flow import Flow as flow

# the components
from .Factory import Factory as factory
from .Product import Product as product

# the decorators
from .Binder import Binder as bind


# the workflow foundry
@pyre.foundry(implements=flow, tip="a container of flow products and factories")
def workflow():
    # get the implementation
    from .Workflow import Workflow
    # borrow its docstring
    __doc__ = Workflow.__doc__
    # and publish it
    return Workflow


# and workflow factory
def newWorkflow(**kwds):
    # get the class
    from .Workflow import Workflow
    # build an instance and return it
    return Workflow(**kwds)


# end of file
