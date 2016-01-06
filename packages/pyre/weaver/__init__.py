# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


"""
This package contains the machinery necessary to generate content in a variety of output formats.

The primary target is human readable formats, such source code for programming languages.
"""


# the marker of component factories
from .. import foundry

# access to the main components in this package
from .Weaver import Weaver as weaver
# the language interface
from .Language import Language as language

# the mill base classes
@foundry(implements=language)
def mill():
    """
    The base mill component
    """
    # grab the component class
    from .Mill import Mill as mill
    # and return it
    return mill

@foundry(implements=language)
def line():
    """
    The base mill component
    """
    # grab the component class
    from .LineMill import LineMill as line
    # and return it
    return line

@foundry(implements=language)
def block():
    """
    The base mill component
    """
    # grab the component class
    from .BlockMill import BlockMill as block
    # and return it
    return block


# access to the known languages
@foundry(implements=language)
def c():
    """
    The C weaver
    """
    # grab the protocol
    from .C import C as c
    # build a facility and return it
    return c

@foundry(implements=language)
def csh():
    """
    The csh weaver
    """
    # grab the protocol
    from .CSh import CSh as csh
    # build a facility and return it
    return csh

@foundry(implements=language)
def cfg():
    """
    The cfg weaver
    """
    # grab the protocol
    from .Cfg import Cfg as cfg
    # build a facility and return it
    return cfg

@foundry(implements=language)
def cxx():
    """
    The C++ weaver
    """
    # grab the protocol
    from .Cxx import Cxx as cxx
    # build a facility and return it
    return cxx

@foundry(implements=language)
def f77():
    """
    The FORTRAN weaver
    """
    # grab the protocol
    from .F77 import F77 as f77
    # build a facility and return it
    return f77

@foundry(implements=language)
def f90():
    """
    The F90 weaver
    """
    # grab the protocol
    from .F90 import F90 as f90
    # build a facility and return it
    return f90

@foundry(implements=language)
def html():
    """
    The HTML weaver
    """
    # grab the protocol
    from .HTML import HTML as html
    # build a facility and return it
    return html

@foundry(implements=language)
def http():
    """
    The HTTP weaver
    """
    # grab the protocol
    from .HTTP import HTTP as http
    # build a facility and return it
    return http

@foundry(implements=language)
def make():
    """
    The make weaver
    """
    # grab the protocol
    from .Make import Make as make
    # build a facility and return it
    return make

@foundry(implements=language)
def perl():
    """
    The perl weaver
    """
    # grab the protocol
    from .Perl import Perl as perl
    # build a facility and return it
    return perl

@foundry(implements=language)
def python():
    """
    The python weaver
    """
    # grab the protocol
    from .Python import Python as python
    # build a facility and return it
    return python

@foundry(implements=language)
def sql():
    """
    The SQL weaver
    """
    # grab the protocol
    from .SQL import SQL as sql
    # build a facility and return it
    return sql

@foundry(implements=language)
def svg():
    """
    The SVG weaver
    """
    # grab the protocol
    from .SVG import SVG as svg
    # build a facility and return it
    return svg

@foundry(implements=language)
def sh():
    """
    The sh weaver
    """
    # grab the protocol
    from .Sh import Sh as sh
    # build a facility and return it
    return sh

@foundry(implements=language)
def tex():
    """
    The TeX weaver
    """
    # grab the protocol
    from .TeX import TeX as tex
    # build a facility and return it
    return tex

@foundry(implements=language)
def xml():
    """
    The XML weaver
    """
    # grab the protocol
    from .XML import XML as xml
    # build a facility and return it
    return xml


# the templater
def smith():
    """
    The templater facility
    """
    # grab the protocol
    from .Smith import Smith as smith
    # build facility and return it
    return smith()

# the protocol that captures the project metadata
from .Project import Project as project

# the templated project implementations
@foundry(implements=project)
def django():
    """
    The django project type
    """
    # grab the protocol
    from .Django import Django as django
    # make a facility and return it
    return django

@foundry(implements=project)
def plexus():
    """
    The plexus project type
    """
    # grab the protocol
    from .Plexus import Plexus as plexus
    # make a facility and return it
    return plexus


# end of file
