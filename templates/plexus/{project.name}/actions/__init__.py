# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# convenient access to the base command class
from .Command import Command as command


# administrivia
def copyright():
    from .Copyright import Copyright
    return Copyright

def credits():
    from .Credits import Credits
    return Credits

def info():
    from .Info import Info
    return Info

def license():
    from .License import License
    return License

def version():
    from .Version import Version
    return Version


# end of file
