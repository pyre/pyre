#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access the framework
import pyre


# declare an abstract specification
class task(pyre.protocol, family='toy.tasks'):

    # types
    from pyre.units.time import hour

    # public state
    duration = pyre.properties.dimensional(default=1*hour)

    # interface
    @pyre.provides
    def perform(self):
        """do something"""

    # framework support
    @classmethod
    def pyre_default(cls):
        return relax


# an actual task
class relax(pyre.component, family='toy.tasks.relax', implements=task):

    duration = pyre.properties.dimensional(default=1*task.hour)
    
    @pyre.export
    def perform(self):
        return "relaxing for {:base={hour},label=hour}".format(self.duration, hour=task.hour)


# another actual task
class study(pyre.component, family='toy.tasks.study', implements=task):

    duration = pyre.properties.dimensional(default=2*task.hour)
    
    @pyre.export
    def perform(self):
        return "studying for {:base={hour},label=hour}".format(self.duration, hour=task.hour)


class patrol(pyre.component, family='toy.tasks.patrol', implements=task):

    duration = pyre.properties.dimensional(default=1.5*task.hour)
    
    @pyre.export
    def perform(self):
        return "patrolling for {:base={hour},label=hour}".format(self.duration, hour=task.hour)


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
