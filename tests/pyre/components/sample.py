#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sample file with component declarations for the tests in this directory
"""


import pyre

# FOR: component_class_binding_implicit.py
# declare a component that implements the job interface
class worker(pyre.component):
    """an implementation"""
    @pyre.export
    def do(self):
        """do something"""


# end of file 
