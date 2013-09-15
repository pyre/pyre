# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# built-in spells

# meta activities
def info():
    from .Info import Info
    return Info

def init():
    from .Initializer import Initializer
    return Initializer

def add():
    from .AssetManager import AssetManager
    return AssetManager


# administrivia
def copyright():
    from .Copyright import Copyright
    return Copyright

def license():
    from .License import License
    return License

def version():
    from .Version import Version
    return Version


# end of file 
