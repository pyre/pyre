#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orhtologue
# (c) 1998-2014 all rights reserved
#


"""
Build the {authorized_keys} file that grants write access to the repository
"""

# externals
import os
# settings
roll = '.'
home = '/home/projects/pyre'
root = os.path.join(home, 'repository')


# build the {authorized_keys} file
def grant():
    """
    Build the {authorized_keys} file
    """
    # create the output file
    authorized = open('authorized_keys', 'w')
    # the command template
    command = (
            'command="bzr serve --inet --directory={} --allow-writes"'.format(root) +
            ',no-port-forwarding,no-X11-forwarding,no-agent-forwarding {}'
            )
    # add the user keys to the file
    authorized.writelines(command.format(key) for user,key in readKeys())
    # close the file
    authorized.close()
    # all done
    return


# read the keys
def readKeys():
    """
    Open all files with the extension {.pub} in the current directory and return all the keys
    they contain
    """
    # for each file in the roll directory
    for filename in os.listdir(roll):
        # extract the name of the user and the extension of the file
        user, ext = os.path.splitext(filename)
        # skip files that do not contain public keys
        if ext != '.pub': continue
        # assemble the path to the key file
        keyfile = os.path.abspath(os.path.join(roll, filename))
        # read the contents
        for key in open(keyfile, 'r'):
            # show me the key
            yield user, key
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    grant()


# end of file 
