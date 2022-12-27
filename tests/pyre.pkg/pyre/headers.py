#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved


# framework
import pyre


# app
class Headers(pyre.application, family="pyre.applications.headers"):

    # user configurable state
    columns = pyre.properties.dict(schema=pyre.properties.int())


    # protocol obligations
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # go through the columns
        for column, offset in self.columns.items():
            # verify they were all converted to integers
            assert type(offset) is int

        # all done
        return 0


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Headers(name="headers")
    # invoke
    status = app.run()
    # share
    raise SystemExit(status)


# end of file
