# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# the framework
import pyre
# my protocol
from .Project import Project


# declaration
class ProjectTemplate(pyre.component, implements=Project):
    """
    Encapsulation of the project information
    """


    # user configurable state
    name = pyre.properties.str(default='project')
    name.doc = "the name of the project"

    authors = pyre.properties.str(default='[ replace with the list of authors ]')
    authors.doc = "the list of project authors"

    affiliations = pyre.properties.str(default='[ replace with the author affiliations ]')
    affiliations.doc = "the author affiliations"

    span = pyre.properties.str(default='[ replace with the project duration ]')
    span.doc = "the project duration for the copyright message"

    template = pyre.properties.str(default=None)
    template.doc = "the project template"

    hostname = pyre.properties.str(default='localhost')
    hostname.doc = "the name of the machine that hosts the live application"

    home = pyre.properties.str(default='~')
    home.doc = "the home directory of the remote user hosting the installation"

    root = pyre.properties.str(default='{project.home}/live')
    root.doc = "the home directory of the remote user hosting the installation"

    web = pyre.properties.str(default='{project.root}/web')
    web.doc = "the location of web related directories at the remote machine"

    admin = pyre.properties.str(default='root')
    admin.doc = "the username of the remote administrator"


# end of file
