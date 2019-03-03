# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import stat, time


# declaration
class InfoStat:
    """
    Mixin that knows how to pull information from {stat} structures
    """

    # meta methods
    def __init__(self, info, **kwds):
        # chain up
        super().__init__(**kwds)
        # if we were not handed any information
        if not info:
            # complain for now
            raise NotImplementedError("'{.uri}': stat node with no info".format(self))

        # file attributes
        self.uid = info.st_uid
        self.gid = info.st_gid
        self.size = info.st_size
        self.permissions = stat.S_IMODE(info.st_mode)
        # timestamps
        self.accessTime = info.st_atime
        self.creationTime = info.st_ctime
        self.modificationTime = info.st_mtime
        # all done
        return


    # debugging support
    def dump(self, channel, indent=''):
        """
        Place the known information about this file in the given {channel}
        """
        channel.line("{}node {}".format(indent, self))
        channel.line("{}  uri: '{.uri}'".format(indent, self))
        channel.line("{}  uid: {.uid}".format(indent, self))
        channel.line("{}  gid: {.gid}".format(indent, self))
        channel.line("{}  size: {.size}".format(indent, self))
        channel.line("{}  permissions: {.permissions:o}".format(indent, self))
        channel.line("{}  access time: {}".format(indent, time.ctime(self.accessTime)))
        channel.line("{}  creation time: {}".format(indent, time.ctime(self.creationTime)))
        channel.line("{}  modification time: {}".format(indent, time.ctime(self.modificationTime)))

        # all done
        return


# end of file
