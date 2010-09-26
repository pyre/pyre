# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

"""
pyre is a framework for building flexible applications

For more details, see http://pyre.caltech.edu.
For terms of use, see pyre.license()
"""


# imported symbols
import os
import weakref


# geography
def home():
    """
    Return the directory of the pyre package
    """
    return os.path.dirname(__file__)


def prefix():
    """
    Compute the pathname of the pyre installation
    """
    return os.path.abspath(os.path.join(home(), os.path.pardir, os.path.pardir))
    

# administrative
def copyright():
    """
    Return the pyre copyright note
    """
    return _pyre_copyright


def license():
    """
    Print the pyre license
    """
    print(_pyre_license)
    return


def version():
    """
    Return the pyre version
    """
    return _pyre_version


# license
_pyre_version = (1, 0, 0)

_pyre_copyright = "pyre: Copyright (c) 1998-2010 Michael A.G. Aïvázis"

_pyre_license = """
    pyre 1.0
    Copyright (c) 1998-2010 Michael A.G. Aïvázis
    All Rights Reserved


    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the
      distribution.

    * Neither the name pyre nor the names of its contributors may be
      used to endorse or promote products derived from this software
      without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
    """


# put these steps inside a function so there is no namespace pollution
def debug():
    """
    Enable debugging of pyre modules

    This must be done very early, before pyre itself starts importing its packages. One way to
    request debugging is to create a variable {pyre_debug} in the __main__ module that contains
    a set of strings, each one of which is the name of a pyre module that you would like to
    debug.
    """
    # the set of packages to patch for debug support
    packages = set()
    # pull pyre_debug from the __main__ module
    import __main__
    try:
        packages |= set(__main__.pyre_debug)
    except:
        pass
    # iterate over the names, import the package and invoke its debug method
    for package in packages:
        module = __import__(package, fromlist=["debug"])
        module.debug()
    # all done
    return


def boot():
    """
    Perform all the initialization steps necessary to bootstrap the framework
    """
    # check the version of python
    import sys
    major, minor, micro, level, serial = sys.version_info
    if major < 3 and minor < 1:
        raise PyreError(description="pyre needs python 3.1 or newer")

    import __main__
    try:
        if __main__.pyre_noboot: return None
    except:
        pass

    # force the creation of the executive singleton
    from . import framework
    p = framework.executive(managers=framework)

    # patch Requirement
    from .components.Requirement import Requirement
    Requirement.pyre_executive = weakref.proxy(p)

    # patch Configurable
    from .components.Configurable import Configurable
    Configurable.pyre_executive = weakref.proxy(p)

    # and return the executive
    return p


def shutdown():
    """
    Attempt to hunt down and destroy all known references to the executive
    """
    # access the executive
    global executive
    # destroy the copy held by the Pyre singleton
    executive.shutdown()
    # and zero out the global reference
    executive = None
    # that should be enough
    return
    

# kickstart
# invoke the debug method in case the user asked for debugging support
debug()
# build the executive
executive = boot()

# gather the exported names
# component declaration support
from . import schema, constraints
from .components import export, provides
from .components import property, facility, interface, component
from .components import properties


# the base class of all pyre exceptions
from .framework.exceptions import PyreError


# end of file 
