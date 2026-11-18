# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .InfoFile import InfoFile


# declaration
class InfoS3(InfoFile):
    """
    The metadata of a filesystem entry that stands for an object in an S3 bucket, as the listing
    of the bucket reports it; a store that leaves a field out of its listing leaves it unset
    """

    # metamethods
    def __init__(self, size=None, modified=None, etag=None, storageClass=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the size of the object, in bytes
        self.size = size
        # when the object was last written, with its time zone
        self.modified = modified
        # the entity tag of the object, as S3 quotes it; the digest of its contents when it was
        # written in one piece, the digest of the digests of its parts, followed by their
        # number, when it was written in parts
        self.etag = etag
        # the storage class of the object, which says whether it can be read right away or must
        # first be restored from an archive
        self.storageClass = storageClass
        # all done
        return


# end of file
