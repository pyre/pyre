#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the merlin shell is accessible
"""


def test():
    # access to the merlin executive
    from merlin import merlin
    # mount the project directory
    merlin.mountProjectDirectory()

    # get the curator
    curator = merlin.curator
    # create a project description object
    project = merlin.newProject(name="test")
    # archive it
    curator.saveProject(project)
    # refresh the folder
    merlin.pyre_executive.fileserver['/merlin/project'].discover()
    # and load it back in
    project = curator.loadProject()

    # check the name
    assert project.name == "test"

    # and return
    return project


# main
if __name__ == "__main__":
    test()


# end of file 
