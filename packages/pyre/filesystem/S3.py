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
        # if it's not a folder
        if not root.isFolder:
            # complain
            raise self.DirectoryListingError(uri=root.uri, error="not a directory")

        # get my bucket
        bucket = self.bucket
        # make a paginator
        paginator = self.s3.get_paginator("list_objects_v2")
        # prime the workload
        todo = [(root, 0)]
        # start walking the bucket contents
        for folder, level in todo:
            # check whether we are deeper in the bucket than the user limit
            if levels is not None and level >= levels:
                # move on
                continue
            # compute the actual location of this folder
            location = self.vnodes[folder].uri
            # project this location relative to my bucket
            prefix = location.address.relativeTo(bucket.address)
            # while the paginator is able to retrieve more contents
            for page in paginator.paginate(
                Bucket=bucket.address.name, Prefix=str(prefix) + "/", Delimiter="/"
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
                    # connect them to the folder we are visiting
                    folder[uri.address.name] = node
                    # build their metadata
                    meta = node.metadata(uri=uri)
                    # and add the metadata to my {vnode} table
                    self.vnodes[node] = meta
                # go through the prefixes
                for entry in prefixes:
                    # these will be folders
                    node = folder.folder()
                    # assemble their uri
                    uri = bucket / entry
                    # connect them to the folder we are visiting
                    folder[uri.address.name] = node
                    # build their metadata
                    meta = node.metadata(uri=uri)
                    # and add the metadata to my {vnode} table
                    self.vnodes[node] = meta
                    # also, add them to the to-do pile along with a level marker so we can
                    # visit them to get their contents
                    todo.append((node, level + 1))

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
