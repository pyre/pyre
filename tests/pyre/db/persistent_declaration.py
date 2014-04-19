#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Exercise the declaration of a persistent object
"""


def test():
    # access to the package
    import pyre.db

    # the schema
    class Entity(pyre.db.table):
        """Entities"""
        eid = pyre.db.str().primary()
        name = pyre.db.str().notNull()

    class Person(Entity, id='persons'):
        """People"""

    class Employer(Entity, id='employers'):
        """Companies"""

    class Employement(pyre.db.table, id="employment"):
        """Relationships between people and companies"""
        eid = pyre.db.str().primary()
        employee = pyre.db.reference(key=Person.eid).notNull()
        employer = pyre.db.reference(key=Employer.eid).notNull()
        rate = pyre.db.float()
        
    # the model
    class Employee(pyre.db.object):
        """
        An object whose attributes are stored in a relational schema
        """

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
