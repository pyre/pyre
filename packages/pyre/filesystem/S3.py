# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


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

    # interface
    def discover(self, prefix=None, **kwds):
        """
        Fill my structure with contents that match {prefix}
        """
        # if the user didn't supply a search prefix
        if prefix is None:
            # use mine
            prefix = self.prefix
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
            channel.line(f"while exploring '{root}'")
            # flush
            channel.log()
            # and bail, in case errors aren't fatal
            return self

        # make a paginator
        paginator = s3.get_paginator("list_objects_v2")
        # set up its options
        options = {
            # the bucket
            "Bucket": self.bucket,
            # the search prefix
            "Prefix": str(prefix),
        }
        # go through the pages
        for page in paginator.paginate(**options):
            # retrieve the contents
            contents = page.get("Contents", [])
            # go through them
            for entry in contents:
                # get each key
                key = entry["Key"]
                # and add it to my pile
                self[key] = self.node()

        # all done
        return self

    # metamethods
    def __init__(self, root, **kwds):
        # build my metadata
        metadata = self.metadata(uri=pyre.primitives.path())
        # chain up
        super().__init__(metadata=metadata, **kwds)

        # deconstruct my root
        profile, region, bucket, prefix = self._parse(uri=root)
        # save my parts
        self.profile = profile
        self.region = region
        self.bucket = bucket
        self.prefix = prefix
        # assemble my location
        self.location = pyre.primitives.uri(
            scheme="s3",
            authority=f"{profile}@{region}",
            address=pyre.primitives.path(f"/{bucket}"),
        )

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
        # if the {profile} is trivial
        if not profile:
            # set it to {default}
            profile = "default"
        # get the profile configuration
        config = pyre.executive.user.aws.profile(name=profile)
        # if the {region} is trivial
        if not region:
            # ask the profile
            region = config.get("region", "")
        # get the address
        address = pyre.primitives.path(uri.address)
        # the bucket is the root
        bucket = address[1]
        # and the rest is the prefix
        prefix = pyre.primitives.path(address[2:])
        # all done
        return profile, region, bucket, prefix


# end of file
