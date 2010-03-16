# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class NameServer(object):

    """
    The manager of the virtual filesystem

    Intances of NameServer manage hierarchical namespaces implemented as a virtual
    filesystem. The contents of these namespaces are retrieved using URIs, and can be arbitrary
    objects, although they are typically either local or remote files.

    The framework uses a NameServer instance to decouple the logical names of resources from
    their physical locations at runtime. For example, as part of the bootstrapping process, the
    frameworks discovers the pyre installation directory; the persistent store for the default
    component configurations is a subdirectory of that location and it is mounted as '/system'
    in the virtual filesystem. This has the following benefits:
    
    * applications can navigate through the contents of '/system' as if it were an actual
      filesystem

    * configuration settings that require references to entries in '/system' can now be
      expressed portably, since there is no need to hardwire actual paths

    Similarly, user preferences are retrieved from '/user', which typically refers to the
    subdirectory '.pyre' of the user's home directory, but may be populated from other sources,
    depending on the operating system.

    Applications are encouraged to lay out their own custom namespaces. The application
    developer can refer to resources through their standardized logical names, whereas the user
    is free to provide the mapping that reflects their physical location at runtime.
    """


# end of file 
