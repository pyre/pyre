# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
This package contains the implementation of the pml reader and writer

A well formed pml document is an XML document that contains the following tags:

  <config>: the top level tag that corresponds to the entire document
  <package>: establishes a namespace for the bindings it contains. 
  <component>: introduces the configuration section for a component
  <bind>: establishes the value of a property

As a simple example,

   <?xml version="1.0" encoding="utf-8"?>
   <config>
       <bind property="pyre.user">Michael Aïvázis</bind>
   </config>

assign the value "Michael Aïvázis" to the property "pyre.user". This is equivalent to supplying

   --pyre.user=Michael Aïvázis

on the command line. If there are many properties in the pyre namespace, you can group them
together inside a package tag, so you don't have to repeat the "pyre." part of the name.

   <?xml version="1.0" encoding="utf-8"?>
   <config>
       <package name="pyre">
           <bind property="user">Michael Aïvázis</bind>
       </package>
   </config>

These two documents have the same net effect on the configuration store. This equivalence is
established by treating the character '.' in the names of properties and packages as a
namespace level separator, similar to the way it is treated on the command line.  Package
tags can nest arbitrarily deeply, with each level adding further qualifications to its parent
namespace.
   
"""


# end of file
