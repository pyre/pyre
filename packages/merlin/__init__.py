# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
"""


def main():
    """
    This is the main entry point in the package. It is invoked by the {merlin} script.  Its job
    is to boot pyre, examine the command line to deduce which actor the user would like to
    invoke, instantiate it, and call its main entry point with the supplied command line
    arguments.

    There are other possible ways to invoke merlin. See the package documentation.
    """
    # let the executive do its thing
    return merlin.run()


# administrative
def usage(**kwds):
    # print the usage screen
    print(_merlin_usage)
    # and return
    return


def version(**kwds):
    """
    Return the merlin version
    """
    # print the version number
    print(_merlin_header)
    # and return
    return


def copyright(**kwds):
    """
    Return the merlin copyright note
    """
    # print the copyright note
    print(_merlin_copyright)
    # and return
    return
    

def license(**kwds):
    """
    Print the merlin license
    """
    # print the license text
    print(_merlin_license)
    # and return
    return


# the actual text 
# NYI: add localized versions of all this
_merlin_version = (1, 0)

_merlin_copyright = (
    "merlin {}.{}: Copyright (c) 1998-2012 Michael A.G. Aïvázis".format(*_merlin_version))

_merlin_header = """
    merlin {}.{}
    Copyright (c) 1998-2012 Michael A.G. Aïvázis
    All rights reserved
    """.format(*_merlin_version)


_merlin_usage = _merlin_header + """
    Basic commands:
        merlin init           make this directory the root of a project
        merlin status         print a summary of the state of a build target
        merlin add            add files or directories to the build system
        merlin build          build a target

        merlin help <topic>   detailed help on topic
        merlin help commands  list all the available commands
        merlin help topics    list all available help topics

        merlin license        terms of use

    Visit http://merlin.orthologue.com for the latest documentation
    """


_merlin_license = _merlin_header + """
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the
      distribution.

    * Neither the name merlin nor the names of its contributors may be
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

# the framework entities
from .components import export, properties, component, protocol

# bootstrapping
def boot():
    # check whether the user has indicated we should skip booting
    try:
        import __main__
        if __main__.merlin_noboot: return None
    # if anything goes wrong
    except:
        # just ignore it and carry on
        pass

    # externals
    import weakref
    # access the executive factory
    from .components.Merlin import Merlin
    # build one and return it
    executive = Merlin(name='merlin.executive')
    # patch components with access to this executive
    component.merlin = weakref.proxy(executive)
    # patch the spell protocol
    from .components.Spell import Spell
    Spell.merlin = weakref.proxy(executive)
    # patch spells with access to this executive
    from .spells.Spell import Spell
    Spell.merlin = weakref.proxy(executive)
    # and return it
    return executive
    

# factories
# for spells
from .spells.Spell import Spell as spell

# convenience
def error(message):
    """
    Generate an error message
    """
    # get the logging mechanism
    import journal
    # build an error message object in my namespace
    error = journal.error('merlin')
    # log and return
    return error.log(message)


def warning(message):
    """
    Generate a warning
    """
    # get the logging mechanism
    import journal
    # build a warning object in my namespace
    warning = journal.warning('merlin')
    # log and return
    return warning.log(message)
        

def info(message):
    """
    Generate an informational message
    """
    # get the logging mechanism
    import journal
    # build an informational message object in my namespace
    info = journal.info('merlin')
    # log and return
    return info.log(message)
        

# the singleton
merlin = boot()

# end of file 
