# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# convenient access to the base command class
from .Command import Command as command

# pull in the command decorators
from .. import foundry, action

# administrivia
@foundry(implements=action)
def copyright():
    from .Copyright import Copyright
    return Copyright

@foundry(implements=action)
def credits():
    from .Credits import Credits
    return Credits

@foundry(implements=action)
def info():
    from .Info import Info
    return Info

@foundry(implements=action)
def license():
    from .License import License
    return License

@foundry(implements=action)
def version():
    from .Version import Version
    return Version


# end of file
