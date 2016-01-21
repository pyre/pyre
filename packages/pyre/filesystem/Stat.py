# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import os
import stat


# my base class
from .Recognizer import Recognizer


# class declaration
class Stat(Recognizer):
    """
    This class provides support for sorting out local filesystem entries based on the lowest
    level of metadata available: the actual representation on the hard disk.

    This recognizer uses {os.stat} for discovering the entries in a given directory. Therefore,
    it handles symbolic links transparently.
    """


    # types
    # the various file types
    from .BlockDevice import BlockDevice
    from .CharacterDevice import CharacterDevice
    from .Directory import Directory
    from .File import File
    from .NamedPipe import NamedPipe
    from .Socket import Socket


    # interface
    @classmethod
    def recognize(cls, entry):
        """
        The most basic file recognition: convert the name of a file into a {Node} descendant
        and decorate it with all the metadata available on the disk.
        """
        # attempt to
        try:
            # pull the information from the hard filesystem
            meta = entry.stat()
        # if something goes wrong
        except (FileNotFoundError, NotADirectoryError):
            # there is nothing further to be done
            return None

        # grab my mode
        mode = meta.st_mode

        # walk through the cases
        if stat.S_ISREG(mode):
            # regular file
            return cls.File(uri=entry, info=meta)
        # otherwise
        elif stat.S_ISDIR(mode):
            # directory
            return cls.Directory(uri=entry, info=meta)
        # otherwise
        elif stat.S_ISSOCK(mode):
            # socket
            return cls.Socket(uri=entry, info=meta)
        # otherwise
        elif stat.S_ISBLK(mode):
            # block device
            return cls.BlockDevice(uri=entry, info=meta)
        # otherwise
        elif stat.S_ISCHR(mode):
            # character device
            return cls.CharacterDevice(uri=entry, info=meta)
        # otherwise
        elif stat.S_ISFIFO(mode):
            # fifo
            return cls.NamedPipe(uri=entry, info=meta)

        # otherwise, we have a bug
        import journal
        # build a message
        msg = "{!r}: unknown file type: mode={}".format(entry, mode)
        # and complain
        return journal.firewall("pyre.filesystem").log(msg)


# end of file
