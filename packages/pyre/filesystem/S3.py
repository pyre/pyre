# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import pyre
import journal

# external
import boto3
import botocore.exceptions

# superclass
from .Filesystem import Filesystem


# the file system factory
class S3(Filesystem):
    """
    A filesystem built out of the contents of an S3 bucket
    """

    # exceptions
    from .exceptions import DirectoryListingError

    # interface
    def location(self):
        """
        Assemble my location
        """
        # get the parts of my uri
        scheme = self.scheme
        profile = self.profile or "default"
        region = self.region
        # assemble the authority
        authority = f"{profile}@{region}"
        # make sure my {address} is a path; clients will want to do arithmetic with it
        address = pyre.primitives.path(f"/{self.bucket}")
        # build the location and return it
        return pyre.primitives.uri(scheme=scheme, authority=authority, address=address)

    def discover(self, root=None, levels=0, **kwds):
        """
        Fill my structure with contents that match {prefix}
        """
        # establish the starting point
        root = self if root is None else root
        # and if it's not a folder
        if not root.isFolder:
            # complain
            raise self.DirectoryListingError(uri=root.uri, error="not a directory")
        # get my bucket
        bucket = self.bucket
        # and set the search delimiter
        delimiter = "/"
        # make a paginator
        paginator = self.s3.get_paginator("list_objects_v2")
        # prime the workload; we'll add subdirectories here as we discover them
        todo = [(root, 0)]
        # start walking the bucket contents
        for folder, level in todo:
            # check whether we are deeper in the bucket than the user limit
            if levels is not None and level >= levels:
                # move on
                continue
            # place the current contents of folder in a pile; we will use this to detect which nodes
            # have been removed since the last time we synced with the s3 bucket so we can clean
            # them up
            dead = set(folder.contents)
            # compute the actual location of this folder
            location = self.vnodes[folder].uri
            # project this location relative to my bucket
            prefix = location.address.relativeTo(bucket.address)
            # while the paginator is able to retrieve more content, ask for it; set the {delimiter}
            # to "/" to ask it to stop fetching entries at the next occurrence of the {delimiter},
            # effectively limiting the search to what we are going to interpret as the contents of a
            # directory; it is also very important to terminate the {prefix} with the {delimiter} so
            # that we find the next one, rather than short circuiting the search to the current
            # level
            for page in paginator.paginate(
                # set the bucket
                Bucket=bucket.address.name,
                # make sure the {prefix} is {delimiter} terminated
                Prefix=str(prefix) + delimiter,
                # and truncate key names to the next occurrence of the {delimiter}
                Delimiter=delimiter,
            ):
                # get the items that are stored at this prefix
                items = [entry["Key"] for entry in page.get("Contents", [])]
                # and extract the prefixes to the rest of the bucket contents, given our delimiter
                # these will become folders in the s3 filesystem
                prefixes = [entry["Prefix"] for entry in page.get("CommonPrefixes", [])]
                # go through the items
                for entry in items:
                    # build nodes for them
                    node = folder.node()
                    # assemble their uri
                    uri = bucket / entry
                    # form the name of the file
                    name = uri.address.name
                    # connect them to the folder we are visiting
                    folder[name] = node
                    # build their metadata
                    meta = node.metadata(uri=uri)
                    # add the metadata to my {vnode} table
                    self.vnodes[node] = meta
                    # and remove this node from the {dead} pile, if it's there
                    dead.discard(name)
                # go through the prefixes
                for entry in prefixes:
                    # these will be folders
                    node = folder.folder()
                    # assemble their uri
                    uri = bucket / entry
                    # form the name by which they are known to their container
                    name = uri.address.name
                    # and connect them to the folder we are visiting
                    folder[name] = node
                    # build their metadata
                    meta = node.metadata(uri=uri)
                    # and add the metadata to my {vnode} table
                    self.vnodes[node] = meta
                    # also, add them to the to-do pile along with a level marker so we can
                    # visit them to get their contents
                    todo.append((node, level + 1))
                    # finally, remove them from the {dead} pile
                    dead.discard(name)
            # now, go through the nodes that are still in the dead pile
            for name in dead:
                # ask {folder} for the node that corresponds to the name
                node = folder[name]
                # remove the node from my {vnode} table
                del self.vnodes[node]
                # and from the folder
                del folder.contents[name]
        # all done
        return self

    # metamethods
    def __init__(self, root, **kwds):
        # deconstruct my root and fill out the missing information
        profile, region, bucket, prefix = self._parse(uri=root)
        # reassemble my {root} uri
        root = pyre.primitives.uri(
            scheme="s3",
            authority=f"{profile}@{region}",
            address=bucket.address / prefix,
        )
        # build my metadata
        metadata = self.metadata(uri=root)
        # and chain up
        super().__init__(metadata=metadata, **kwds)

        # save my parts
        # scheme
        self.scheme = "s3"
        # authority
        self.profile = profile
        self.region = region
        # the complete uri of my bucket
        self.bucket = bucket
        # and the path to my prefix
        self.prefix = prefix

        # attempt to
        try:
            # connect
            s3 = boto3.Session(
                profile_name=self.profile, region_name=self.region
            ).client("s3")
        # if something goes wrong
        except botocore.exceptions.BotoCoreError as error:
            # make a channel
            channel = journal.error("pyre.filesystem.s3")
            # complain
            channel.line(f"got: {error}")
            channel.line(f"while exploring '{self.location()}'")
            # flush
            channel.log()
            # and bail, in case errors aren't fatal
            return
        # if all goes well, save the s3 connection
        self.s3 = s3

        # all done
        return

    # implementation details
    @classmethod
    def _parse(cls, uri):
        """
        Deconstruct {uri} into a form suitable for my metadata
        """
        # coerce the input into a uri
        uri = pyre.primitives.uri.parse(value=uri, scheme="s3")
        # unpack the server info
        region, _, profile, _ = uri.server
        # get the profile configuration
        config = pyre.executive.user.aws.profile(name=profile or "default")
        # if the {region} is trivial
        if not region:
            # ask the profile
            region = config.get("region", "")
        # get the address
        address = pyre.primitives.path(uri.address)
        # the bucket is the root; convert it into a complete uri
        bucket = pyre.primitives.uri(
            scheme=uri.scheme,
            authority=f"{profile}@{region}",
            address=pyre.primitives.path(address[:2]),
        )
        # and the rest is the prefix path
        prefix = address[2:]
        # if it's non-trivial, turn it into a path
        prefix = pyre.primitives.path(prefix) if prefix else pyre.primitives.path.root
        # all done
        return profile, region, bucket, prefix


# end of file
