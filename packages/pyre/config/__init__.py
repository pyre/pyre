# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


# factories
def newConfigurator(**kwds):
    from .Configurator import Configurator
    return Configurator(**kwds)


def newEvaluator(**kwds):
    from .Evaluator import Evaluator
    return Evaluator(**kwds)


# end of file 
