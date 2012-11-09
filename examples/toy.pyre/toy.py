#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access the framework
import pyre


# declare an abstract specification
class task(pyre.protocol, family='toy.tasks'):

    duration = pyre.properties.float(default=60)

    @pyre.provides
    def perform(self):
        """do something"""

    @classmethod
    def pyre_default(cls):
        return relax


# an actual task
class relax(pyre.component, family='toy.tasks.relax', implements=task):

    duration = pyre.properties.float(default=60)
    
    @pyre.export
    def perform(self):
        return "relaxing for {} minutes".format(self.duration)


# another actual task
class study(pyre.component, family='toy.tasks.study', implements=task):

    duration = pyre.properties.float(default=120)
    
    @pyre.export
    def perform(self):
        return "studying for {} minutes".format(self.duration)


class patrol(pyre.component, family='toy.tasks.patrol', implements=task):

    duration = pyre.properties.float(default=75)
    
    @pyre.export
    def perform(self):
        return "patrolling for {} minutes".format(self.duration)


# a specification for people categories
class people(pyre.protocol, family='toy.people'):

    activities = pyre.properties.list(schema=task())

    @pyre.provides
    def perform(self):
        """perform my specified activities"""


# an actual person category
class person(pyre.component, implements=people):

    activities = pyre.properties.list(schema=task())

    @pyre.export
    def perform(self):
        """perform my activities"""
        for activity in self.activities: yield activity.perform()


# students
class student(person, family='toy.people.student'):

    foo = task()
    activities = pyre.properties.list(schema=task(default=relax))


# policemen
class policeman(person, family='toy.people.policeman'):

    activities = pyre.properties.list(schema=task(default=patrol))


# end of file 
