#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""

def test():

    from pyre.filesystem.exceptions import (
        GenericError, DirectoryListingError, MountPointError, FilesystemError,
        FolderError, NotFoundError, FolderInsertionError, URISpecificationError
        )

    try:
        raise GenericError(description=None)
    except GenericError as error:
        pass

    try:
        raise DirectoryListingError(uri=None, error=None)
    except DirectoryListingError as error:
        pass

    try:
        raise MountPointError(uri=None, error=None)
    except MountPointError as error:
        pass

    try:
        raise FilesystemError(filesystem=None, node=None, description=None)
    except FilesystemError as error:
        pass

    try:
        raise FolderError(uri=None, fragment=None, filesystem=None, node=None)
    except FolderError as error:
        pass

    try:
        raise NotFoundError(uri=None, fragment=None, filesystem=None, node=None)
    except NotFoundError as error:
        pass

    try:
        raise FolderInsertionError(uri=None, target=None, filesystem=None, node=None)
    except FolderInsertionError as error:
        pass

    try:
        raise URISpecificationError(uri=None, reason=None)
    except URISpecificationError as error:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
