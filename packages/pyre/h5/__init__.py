# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import pyre
import journal

# internals that mirror the h5 C++ api
from .Identifier import Identifier as identifier
from .Location import Location as location
from .Object import Object as object

# structural objects
from .Group import Group as group
from .File import File as file


# datasets
from .Dataset import Dataset as dataset

# scalars
bool = dataset.bool
float = dataset.float
int = dataset.int
str = dataset.str
timestamp = dataset.timestamp
# containers
array = dataset.array
list = dataset.list
tuple = dataset.tuple

# containers
from .typed.Strings import Strings as strings


# readers and writers
from .Reader import Reader as reader
from .Writer import Writer as writer

# visitors
from .Explorer import Explorer as explorer
from .Tree import Tree as tree
from .Walker import Walker as walker


# file factory
def open(uri: pyre.primitives.uri, mode: str = "r"):
    """
    Open the file given its {uri}
    """
    # parse the {uri}
    uri = pyre.primitives.uri.parse(value=uri, scheme="file")

    # if the scheme is {file}
    if uri.scheme == "file":
        # make a local file object whose path is the address in the {uri}
        f = file().open(uri=uri.address, mode=mode)
        # and return it
        return f

    # if the scheme is {s3}
    if uri.scheme == "s3":
        # if the library doesn't have support for {ros3}
        if not pyre.libh5.ros3():
            # make a channel
            channel = journal.error("pyre.h5.file")
            # complain
            channel.line("this installation of libhdf5 has no support for ros3")
            channel.line(f"while looking for '{uri}'")
            # flush
            channel.log()
            # and bail
            return None
        # we interpret the {authority} field as the bucket name
        authority = uri.authority
        # so it must be there
        if authority is None:
            # make a channel
            channel = journal.error("pyre.h5.open")
            # complain
            channel.line("couldn't figure out the bucket name")
            channel.line(f"while looking for '{uri}'")
            # flush
            channel.log()
            # and bail, in case errors aren't fatal
            return None

        # if it's there, take it apart
        fields = uri.authority.split("@")
        # extract the authentication profile and the name of the S3 bucket
        profile, bucket = fields if len(fields) == 2 else "", uri.authority
        # get the object key
        key = uri.address
        # open the remote dataset with the {ros3} driver
        f = file().ros3(bucket=bucket, key=key)
        # and return it
        return f

    # if we get this far, the {uri} was malformed; make a channel
    channel = journal.error("pyre.h5")
    # and complain
    channel.log(f"unknown scheme in dataset '{uri}'")

    # all done
    return


# end of file
