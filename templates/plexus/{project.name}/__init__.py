# -*- Python -*-
# -*- coding: utf-8 -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


# import and publish pyre symbols
from pyre import (
    # protocols, components and traits
    schemata, constraints, properties, protocol, component, foundry,
    # decorators
    export, provides,
    # the manager of the pyre runtime
    executive,
    # miscellaneous
    tracking, units
    )


# bootstrap
package = executive.registerPackage(name='{project.name}', file=__file__)
# save the geography
home, prefix, defaults = package.layout()

# publish local modules
from . import (
    meta, # meta-data
    extensions, # my extension module
    )

# plexus support
from .components import plexus, action, command


# end of file
