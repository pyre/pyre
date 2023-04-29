# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# declaration
class Complete(merlin.shells.command, family="merlin.cli.complete"):
    """
    Assist with shell auto-completion
    """

    word = merlin.properties.str()
    word.doc = "the word we are attempting to auto-complete"

    line = merlin.properties.str()
    line.doc = "the partial command line"


    # administrative
    @merlin.export(tip="generate completions candidates from a partial command line")
    def main(self, plexus, argv, **kwds):
        """
        Suggest possible completions for the partial argument list
        """
        # ask the plexus for the names of all public actions
        actions = plexus.pyre_action.pyre_documentedActions(plexus=plexus)
        # collect their names
        names = tuple(name for _, name, _, _ in actions)

        # get the args
        args = self.line.split()
        # and the partial word
        word = self.word

        # if there is only one entry
        if len(args) == 1:
            # go through all the names
            for name in names:
                # and print them out
                print(name)
            # all done
            return 0

        # if there are two entries and a partial word
        if len(args) == 2 and word:
            # go through the names
            for name in names:
                # if this name starts with the partial word
                if name.startswith(self.word):
                    # it's a candidate; print it
                    print(name)
            # all done
            return 0

        # if there are two entries and the partial word is empty
        if len(args) == 2 and not word:
            # get the name of the action
            action = args[1]
            # if it's not known
            if action not in names:
                # bail
                return 1
            # otherwise, instantiate it
            command = plexus.pyre_repertoire.resolve(plexus=plexus, spec=action)
            # go through its traits
            for trait in command.pyre_behaviors():
                # get the name
                name = trait.name
                # and the tip
                tip = trait.tip
                # if the trait has no name or no tip
                if not name or not tip:
                    # skip it
                    continue
                # otherwise, print the name
                print(name)
            # all done
            return 0

        # if there are three entries and the partial word is not empty
        if len(args) == 3 and word:
            # get the name of the action
            action = args[1]
            # if it's not known
            if action not in names:
                # bail
                return 1
            # otherwise, instantiate it
            command = plexus.pyre_repertoire.resolve(plexus=plexus, spec=action)
            # go through its traits
            for trait in command.pyre_behaviors():
                # get the name
                name = trait.name
                # and the tip
                tip = trait.tip
                # if the trait has no name or no tip
                if not name or not tip:
                    # skip it
                    continue
                # if the name does not start with the partial word
                if not name.startswith(word):
                    # also skip it
                    continue
                # otherwise, print the name
                print(name)
            # all done
            return 0

        # all done
        return 0


# end of file
