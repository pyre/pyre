# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# attempt to
try:
    # load the extension module
    from pyre.extensions import cuda
# if this fails
except ImportError:
    # not much to do...
    msg = "could not load the 'cuda' extension module"
    # complain
    import journal
    raise journal.error('cuda').log(msg)


# otherwise, all is well;
# pull in the administrivia
version = cuda.version
copyright = cuda.copyright
def license() : print(cuda.license())


# build the device manager
from .DeviceManager import DeviceManager
manager = DeviceManager(extension=cuda)


# end of file
