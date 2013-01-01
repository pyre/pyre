# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import os
import merlin


# declaration
class PythonClassifier(merlin.component):
    """
    An asset classifier that recognizes modules, packages and extensions
    """


    # types: the python asset factories
    from ..assets import pythonmodule, pythonpackage


    # interface
    def classify(self, root, node):
        """
        Explore {node}, assuming it is an instance of a {pyre.filesystem.Node} subclass,
        looking for assets
        """
        # get the node uri relative to the root of the project
        uri = os.path.relpath(node.uri, root)
        # take apart the node uri
        path, filename = os.path.split(node.uri)
        # if the node is a file
        if not node.isFolder:
            # extract its name and extension
            name, ext = os.path.splitext(filename)
            # if it's not a python source file, return empty handed
            if not ext == '.py': return None
            # otherwise
            return self.pythonmodule(name=name, uri=uri)
            
        # otherwise it is a folder; if it contains a '__init__.py'
        if node.isFolder and '__init__.py' in node.contents:
            # it is a python package
            package = self.pythonpackage(name=filename, uri=uri)
            # populate it
            for child in node.contents.values():
                # classify it
                asset = self.classify(root=root, node=child)
                # if it couldn't be identified, skip it
                if asset is None: continue
                # otherwise, add it to my contents
                package.contents[asset.name] = asset
            # and hand it to the caller
            return package
    
        # if everything fails, return empty handed
        return None


# end of file 
