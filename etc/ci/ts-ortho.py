#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved
#


# externals
import csv
import os
# the framework
import pyre


# the app
class TSOrtho(pyre.application):
    """
    A utility that checks a set of test suites for orthogonality, defined as the presence of
    identically named test cases
    """


    # user configurable state
    out = pyre.properties.ostream(default="ts-ortho.csv")
    out.doc = "the name of the output file"

    targets = pyre.properties.strings()
    targets.default = ["journal.lib", "journal.pkg", "journal.ext", "journal.api"]
    targets.doc = "the set of test suites to check for orthogonality"


    # obligation
    @pyre.export
    def main(self):
        """
        The entry point
        """
        # mount a filesystem in the {cwd}
        cwd = pyre.filesystem.local(root=".").discover(levels=2)
        # show me
        # print('\n'.join(cwd.dump()))

        # initialize our table
        table = pyre.patterns.vivify(levels=2)
        # we care about the following folders
        targets = self.targets
        # go through them
        for target in targets:
            # look up the folder
            folder = cwd[target]
            # go through its contents
            for name in folder.contents:
                # remove the extension
                name, _ = os.path.splitext(name)
                # mark
                table[name][target] = True

        # attach our output stream to a csv writer
        writer = csv.writer(self.out)

        # build the headers
        writer.writerow([''] + targets)

        # go through the filenames
        for name in sorted(table.keys()):
            # grab the bin
            bin = table[name]
            # build the record
            record = [ 'x' if folder in bin else '' for folder in targets ]
            # write it out
            writer.writerow([name] + record)

        # all done
        return


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = TSOrtho(name="ts-ortho")
    # run
    status = app.run()
    # share
    raise SystemExit(status)


# end of file
