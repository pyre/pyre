#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""

def test():

    from pyre.filesystem.exceptions import (
        GenericError, DirectoryListingError, MountPointError, FilesystemError, NotFoundError,
        FolderInsertionError, URISpecificationError
        )

    try:
        raise GenericError(description=None)
    except GenericError as error:
        pass

    try:
        raise DirectoryListingError(path=None, error=None)
    except DirectoryListingError as error:
        pass

    try:
        raise MountPointError(path=None, error=None)
    except MountPointError as error:
        pass

    try:
        raise FilesystemError(filesystem=None, node=None, description=None)
    except FilesystemError as error:
        pass

    try:
        raise NotFoundError(path=None, fragment=None, filesystem=None, node=None)
    except NotFoundError as error:
        pass

    try:
        raise FolderInsertionError(path=None, target=None, filesystem=None, node=None)
    except FolderInsertionError as error:
        pass

    try:
        raise URISpecificationError(uri=None, description=None)
    except URISpecificationError as error:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
