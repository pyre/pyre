# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
    def recognize(self, entry):
        """
        The most basic file recognition: convert the name of a file into an Node descendant
        and decorate it with all the metadata available on the disk.
        """

        # pull the information from the hard filesystem
        meta = os.stat(entry)
        mode = meta.st_mode

        # walk through the cases
        if stat.S_ISREG(mode):
            return self.File(uri=entry, info=meta)
        elif stat.S_ISDIR(mode):
            return self.Directory(uri=entry, info=meta)
        elif stat.S_ISSOCK(mode):
            return self.Socket(uri=entry, info=meta)
        elif stat.S_ISBLK(mode):
            return self.BlockDevice(uri=entry, info=meta)
        elif stat.S_ISCHR(mode):
            return self.CharacterDevice(uri=entry, info=meta)
        elif stat.S_ISFIFO(mode):
            return self.NamedPipe(uri=entry, info=meta)
        # otherwise
        import journal
        msg = "{!r}: unknown file type: mode={}".format(entry, mode)
        return journal.firewall("pyre.filesystem").log(msg)


# end of file 
