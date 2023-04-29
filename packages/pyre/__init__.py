# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
pyre is a framework for building flexible applications

For more details, see http://pyre.orthologue.com.
For terms of use, see pyre.license()
"""

# check the version of python
import sys
major, minor, micro, _, _ = sys.version_info
# pack it
current = (major, minor,  micro)
# minimum required
required = (3, 7, 2)
# check
if current < required:
    # get the exception type
    from .framework.exceptions import PyreError
    # stringify the required version
    required = '.'.join(map(str, required))
    # and complain
    raise RuntimeError(f"pyre requires python {required} or newer")


# convenience
def resolve(uri):
    """
    Interpret {uri} as a request to locate and load a component
    """
    # build a locator
    caller = tracking.here(level=1)
    # get the executive to retrieve candidates
    for component in executive.resolve(uri=uri):
        # adjust its locator
        component.pyre_locator = tracking.chain(caller, component.pyre_locator)
        # and return it
        return component
    # otherwise, the {uri} could not be resolved
    return


def loadConfiguration(uri):
    """
    Open {uri} and attempt to load its contents into the configuration model
    """
    # build a locator for these settings
    here = tracking.here(level=1)
    # get the executive to do its thing
    return executive.loadConfiguration(uri=uri, locator=here)


# version dependent constants
def computeCallerStackDepth():
    """
    Compute the stack depth offset to get to the caller of a function
    """
    # computed in {tracking}
    return tracking.callerStackDepth


# administrative

def copyright():
    """
    Return the pyre copyright note
    """
    return print(meta.header)


def license():
    """
    Print the pyre license
    """
    # print it
    return print(meta.license)


def version():
    """
    Return the pyre version
    """
    return meta.version


def credits():
    """
    Print the acknowledgments
    """
    # print it
    return print(meta.acknowledgments)


def packageInfo():
    """
    Gather information about the pyre layout
    """
    # first the easy ones
    info = {
        "version": version(),
        "prefix": prefix,
        "path": prefix / "bin",
        "ldpath": prefix / "lib",
        "pythonpath" : home.parent,
        "includes": f"-I{prefix}/include"
        }

    # the libraries
    libs = [ "pyre", "journal" ]
    # get the host
    host = executive.host
    # if the host is a linux box
    if isinstance(host, platforms.linux()):
        # we have to link against the real time clock library
        libs.append("rt")
    # assemble the libraries
    libs = " ".join(f"-l{lib}" for lib in libs)
    # attach
    info["libs"] = f"-L{prefix}/lib {libs}"

    # all done
    return info


# component introspection
def where(configurable, attribute=None):
    """
    Retrieve the location where the {attribute} of {configurable} got its value; if no
    {attribute} is specified, retrieve information about the {configurable} itself
    """
    # if no attribute name is given, return the locator of the configurable
    if attribute is None: return configurable.pyre_locator
    # retrieve the trait descriptor
    trait = configurable.pyre_trait(alias=attribute)
    # grab the locator of the slot where the attribute value is stored
    locator = configurable.pyre_inventory.getTraitLocator(trait)
    # and return it
    return locator


# put the following start-up steps inside functions so we can have better control over their
# execution context and namespace pollution
def boot():
    """
    Perform all the initialization steps necessary to bootstrap the framework
    """
    # check whether the user has indicated we should skip booting
    try:
        import __main__
        if __main__.pyre_noboot: return None
    # if anything goes wrong
    except:
        # just ignore it and carry on
        pass

    # now, check whether
    try:
        # the user has prohibited loading the extension module
        without_libpyre = __main__.pyre_without_libpyre
    # if there is no such setting
    except AttributeError:
        # assume that this means we should try
        without_libpyre = False

    # access the module level variable
    global libpyre
    # if we are not supposed to load the bindings
    if without_libpyre:
        # mark it
        libpyre = None
    # otherwise
    else:
        # pull the bindings, if they exist
        from .extensions import libpyre

    # grab the executive factory
    from . import framework
    # build one and return it
    return framework.executive().boot()


def debug():
    """
    Enable debugging of pyre modules.

    Modules that support debugging must provide a {debug} method and do as little as possible
    during their initialization. The fundamental constraints are provided by the python import
    algorithm that only gives you a single chance to import a module.

    This must be done very early, before pyre itself starts importing its packages. One way to
    request debugging is to create a variable {pyre_debug} in the __main__ module that contains
    a set of strings, each one of which is the name of a pyre module that you would like to
    debug.
    """
    # the set of packages to patch for debug support
    packages = set()
    # get the __main__ module
    import __main__
    # attempt to
    try:
        # get the list of module names specified in the user's main script
        packages |= set(__main__.pyre_debug)
    # if there aren't any
    except:
        # no worries
        pass

    # go through the module names
    for package in packages:
        # import each one
        module = __import__(package, fromlist=["debug"])
        # and invoke its debug method
        module.debug()

    # all done
    return


# kickstart
libpyre = None
# invoke the debug method in case the user asked for debugging support
debug()

# version info
from . import meta
# convenient access to parts of the framework
from . import constraints, geometry, primitives, tracking
# configurables and their support
from .components.Actor import Actor as actor
from .components.Role import Role as role
from .components.Protocol import Protocol as protocol
from .components.Component import Component as component
from .components.Foundry import Foundry as foundry
from .components.Monitor import Monitor as monitor
from .components.Tracker import Tracker as tracker
# traits
from .traits import properties
property = properties.identity
from .traits.Behavior import Behavior as export
from .traits.Behavior import Behavior as provides
from .traits.Facility import Facility as facility

# the base class of all pyre exceptions
from .framework.exceptions import PyreError

# build the executive
executive = boot()
# if the framework booted properly
if executive:
    # low level stuff
    from .extensions import libh5
    # package managers
    from . import externals
    # platform managers
    from . import platforms
    # application shells
    from .shells import application, action, plexus, command, panel
    # support for filesystems
    from . import filesystem
    # hdf5
    from . import h5
    # workflows
    from . import flow
    # document rendering
    from . import weaver
    # the interprocess communication mechanisms
    from . import ipc, nexus, services

    # discover information about the runtime environment
    executive.discover()
    # and turn on the executive
    executive.activate()

    # register this package
    package = executive.registerPackage(name='pyre', file=__file__)
    # and record its geography
    home, prefix, defaults = package.layout()


# clean up the executive instance when the interpreter shuts down
import atexit
@atexit.register
def shutdown():
    """
    Attempt to hunt down and destroy all known references to the executive
    """
    # access the executive
    global executive
    # if there is one
    if executive:
        # ask it to clean up after itself
        executive.shutdown()
        # zero out the global reference
        executive = None
    # that should be enough
    return


# end of file
