# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# built-in spells
from .. import foundry
from .Spell import Spell as spell

# meta activities
@foundry(implements=spell)
def info():
    from .Info import Info
    return Info

@foundry(implements=spell)
def init():
    from .Initializer import Initializer
    return Initializer

@foundry(implements=spell)
def add():
    from .AssetManager import AssetManager
    return AssetManager


# administrivia
@foundry(implements=spell)
def copyright():
    from .Copyright import Copyright
    return Copyright

@foundry(implements=spell)
def license():
    from .License import License
    return License

@foundry(implements=spell)
def version():
    from .Version import Version
    return Version


# end of file
